void calc_sppspe(const string& name, trim_map_sample_block_hook& hook, int* wls, int reads_per_wl)
{
    
// Calculate median Vt after customer erase, single pulse program, and single pulse erase for each WL, SB, and block combination

	vector<block_t> blocks;
	const int num_blocks = hook.blocks(blocks);
	// (no stuck bits in the data) const int remove_stuck_bits = 1;
	const mask& cur = flow_data->functional_mask();
	const int num_block_segments = apg_num_block_segments();
	int num_wls = 0;
	for (int wli = 0; wls[wli] > 0; ++wli) num_wls++;
	const string shmoo_trim = "R_TSS_EDGE_RBASE";

	
	if (pcn){
		stringstream wl_ss; wl_ss << "W(" << ((wls[0] < 10) ? "0" : "") << wls[0];
		for (int wli = 1; wls[wli] != -1; ++wli) { wl_ss << '|'; if (wls[wli] < 10) wl_ss << '0'; wl_ss << wls[wli]; }
		wl_ss << ")";

		//Add trends
		{ stringstream ss; ss << name << "_VT_MED_" << wl_ss.str(); add_trend(ss.str(), __func__); }

	//Add series
	{ stringstream ss; ss << eop_name << "_VT_MED_PER_BLK_" << wl_ss.str(); add_series(num_blocks, ss.str(), __func__); }
	return;
	}
	if (init || skipcalc || !cur.active()) return;

	Dac* read_dac = trim_data->get_trim_info(shmoo_trim.c_str())->dac;

	// Grab data
	string ers_keyword = name + "_ERS_BITS";
	count_result_map::iterator ers_bitsi = count_results.find(ers_keyword);
	if (ers_bitsi == count_results.end()){
      job_error("could not find bits\n");  
    } 
	const count_result& stuck_bits_result = (*ers_bitsi).second;

	string eop_keyword = eops2p_name + "_EOP_BITS";
	count_result_map::iterator eop_bitsi = count_results.find(eop_keyword);
	if (eop_bitsi == count_results.end()) job_error("could not find bits\n");
	const count_result& eop_bits_result = (*eop_bitsi).second;

	// Set up data structures
	multi_series_result<string, double> sig_results;
	if (num_top_sigmas) {
		sig_results.init(num_wls*num_top_sigmas, num_blocks, nan(""));
		sig_results.set_keyword(eop_name + string("_SIG"));
		for (int top_sigma = 0; top_sigma < num_top_sigmas; ++top_sigma) {
			for (int wli = 0; wls[wli] > 0; ++wli) {
				int mi = top_sigma*num_wls + wli;
				stringstream wl_num; wl_num << std::setw(2) << std::setfill('0') << wls[wli];
				stringstream wl_ss; wl_ss << "_W" << wl_num.str();
				stringstream ss; ss << "_" << top_sigma_str[top_sigma] << "_PER_BLK" << wl_ss.str();
				sig_results.set_key(mi, ss.str());
				sig_results.set_skipprint(mi, skipprintifnan);
			}
		}
	}

	multi_series_result<string, double> vt_med_results, pvs_ofst_results, pvs_pm3p5s_results;
	vt_med_results.init(num_wls, num_blocks, nan("")); pvs_ofst_results.init(num_wls, num_blocks, nan("")); pvs_pm3p5s_results.init(num_wls, num_blocks, nan(""));
	vt_med_results.set_keyword(eop_name + string("_VT_MED_PER_BLK"));
	pvs_ofst_results.set_keyword(eop_name + string("_PVS_OFST_3P5S_PER_BLK"));
	pvs_pm3p5s_results.set_keyword(eop_name + string("_PVS_PM3P5S_PER_BLK"));
	for (int wli = 0; wls[wli] > 0; ++wli) {
		stringstream wl_num; wl_num << std::setw(2) << std::setfill('0') << wls[wli];
		stringstream wl_ss; wl_ss << "_W" << wl_num.str();
		vt_med_results.set_key(wli, wl_ss.str()); pvs_ofst_results.set_key(wli, wl_ss.str()); pvs_pm3p5s_results.set_key(wli, wl_ss.str());
		vt_med_results.set_skipprint(wli, skipprintifnan);
		pvs_ofst_results.set_skipprint(wli, skipprintifnan);
		pvs_pm3p5s_results.set_skipprint(wli, skipprintifnan);
	}

	// Calculations
	const int num_reads = eop_bits_result.num_values_per_block();
	for (mask::const_iterator si = cur.begin(); si != cur.end(); ++si) {
		const int head = (*si).head, site = (*si).site;
		const int s = (*si).head * MAX_SITES_PER_HEAD + (*si).site;
		ostream& os = flow_data->log(head, site);

		for (int wli = 0; wls[wli] > 0; ++wli) {
			stringstream wl_num; wl_num << std::setw(2) << std::setfill('0') << wls[wli];
			stringstream wl_ss; wl_ss << "_W" << wl_num.str();
			int ri_start = wli * reads_per_wl;
			int ri_stop = ri_start + reads_per_wl;

			vector< vector<double> >  eop_sig_all(num_top_sigmas);	//eop_vt_all(num_top_sigmas),
			vector<double> offset_3p5_all, eop_vt_med_all, pvs_pm3p5s_all;
			for (int b = 0; b < num_blocks; ++b) {
				stringstream suffix; suffix << wl_ss.str() << "_B" << b;

				// Calculate total block eop_fbc for each read
				int num_good_seg = 0;
				vector<int> eop_fbc(num_reads);
				for (int ri = ri_start; ri < ri_stop && ri < num_reads; ++ri) {
					int blk_fbc = 0;
					for (int seg = 0; seg < num_block_segments; ++seg) {
						if (!valid_sample_block_segment(blocks, s, b, seg)) continue;
						blk_fbc += eop_bits_result.value(s, b, seg, ri);
						++num_good_seg;
					}
					eop_fbc[ri] = blk_fbc;
				}
				if (!num_good_seg) break;

				// Calculate stuck bits for block
				int total_bits = 0, stuck = 0;
				for (int seg = 0; seg < num_block_segments; ++seg) {
					if (!valid_sample_block_segment(blocks, s, b, seg)) continue;
					stuck += stuck_bits_result.value(s, b, seg, wli);
					total_bits += NUM_DS_FL_BITS_PER_BLK_SEG;
				}
				if (!remove_stuck_bits) stuck = 0;

				// Get median Vt
				double eop_vt_med = 0.0;
				int eop_fbc_med = (int)(0.5*(total_bits - stuck)) + stuck;
				for (int ri = ri_start; ri < ri_stop && ri < num_reads; ++ri) {
					if (eop_fbc_med >= eop_fbc[ri]) {
						eop_vt_med = read_dac->to_analog(s, hook.shmoo_trim_value(s, shmoo_trim, ri % reads_per_wl));
						eop_vt_med_all.push_back(eop_vt_med);
						vt_med_results.set(s, wli, b, eop_vt_med);
						break;
					}
				} // read

				// Get top_sigma vts and deltas
				for (int top_sigma = 0; top_sigma < num_top_sigmas; ++top_sigma) {
					int mi = top_sigma*num_wls + wli;
					int tgt = (int)(top_sigmas[top_sigma] * (total_bits - stuck)) + stuck;
					for (int ri = ri_start; ri < ri_stop && ri < num_reads; ++ri) {
						if (tgt >= eop_fbc[ri]) {
							double vt = read_dac->to_analog(s, hook.shmoo_trim_value(s, shmoo_trim, ri % reads_per_wl));
							double sig = vt - eop_vt_med;
							//eop_vt_all[top_sigma].push_back(vt);
							eop_sig_all[top_sigma].push_back(sig);
							sig_results.set(s, mi, b, sig);
							break;
						}
					} // read
				} // top_sigma

				double vt_p1s = 10.0; // Get 1 sig Vt
				int fbc_p1s = (int)(0.15865*(total_bits - stuck)) + stuck;
				for (int ri = ri_start; ri < ri_stop && ri < num_reads; ++ri) {
					if (fbc_p1s >= eop_fbc[ri]) {
						vt_p1s = read_dac->to_analog(s, hook.shmoo_trim_value(s, shmoo_trim, ri % reads_per_wl));
						break;
					}
				} // read

				double vt_3p5s = 10.0; // Get 3.5 sig Vt
				int fbc_3p5s = (int)(0.00024*(total_bits - stuck)) + stuck; //99976
				for (int ri = ri_start; ri < ri_stop && ri < num_reads; ++ri) {
					if (fbc_3p5s >= eop_fbc[ri]) {
						vt_3p5s = read_dac->to_analog(s, hook.shmoo_trim_value(s, shmoo_trim, ri % reads_per_wl));
						break;
					}
				} // read

				double d_3P5Sig_med = vt_3p5s - eop_vt_med;
				double d_1P0Sig_med = vt_p1s - eop_vt_med;
				double pvs_offset_3p5s = d_3P5Sig_med - (d_1P0Sig_med * 3.5);
				if (vt_p1s < 10.0 && vt_3p5s < 10.0) {
					offset_3p5_all.push_back(pvs_offset_3p5s);
					pvs_ofst_results.set(s, wli, b, pvs_offset_3p5s);
				}

				double pvs_pm3p5sigma = (d_1P0Sig_med * 7) + pvs_offset_3p5s;
				pvs_pm3p5s_all.push_back(pvs_pm3p5sigma);
				pvs_pm3p5s_results.set(s, wli, b, pvs_pm3p5sigma);

			} // block


			if (size_t size = eop_vt_med_all.size()) {
				sort(eop_vt_med_all.begin(), eop_vt_med_all.end());
				double eop_vt_med = size % 2 ? eop_vt_med_all[size / 2] : (eop_vt_med_all[size / 2] + eop_vt_med_all[size / 2 - 1]) / 2;
				os << eop_name << "_VT_MED" << wl_ss.str() << " " << eop_vt_med << std::endl;
			}

			if (size_t size = offset_3p5_all.size()) {
				sort(offset_3p5_all.begin(), offset_3p5_all.end());
				double offset_3p5 = size % 2 ? offset_3p5_all[size / 2] : (offset_3p5_all[size / 2] + offset_3p5_all[size / 2 - 1]) / 2;
				os << eop_name << "_PVS_OFST_3P5S" << wl_ss.str() << " " << offset_3p5 << std::endl;
			}

			if (size_t size = pvs_pm3p5s_all.size()) {
				sort(pvs_pm3p5s_all.begin(), pvs_pm3p5s_all.end());
				double pvs_pm3p5s = size % 2 ? pvs_pm3p5s_all[size / 2] : (pvs_pm3p5s_all[size / 2] + pvs_pm3p5s_all[size / 2 - 1]) / 2;
				os << eop_name << "_PVS_PM3P5S" << wl_ss.str() << " " << pvs_pm3p5s << std::endl;
			}

			for (int top_sigma = 0; top_sigma < num_top_sigmas; ++top_sigma) {
				//if(int size = eop_vt_all[top_sigma].size()) {
				//  sort(eop_vt_all[top_sigma].begin(), eop_vt_all[top_sigma].end());
				//  double eop_vt = size % 2 ? eop_vt_all[top_sigma][size/2] : (eop_vt_all[top_sigma][size/2] + eop_vt_all[top_sigma][size/2-1])/2;
				//  os << eop_name << "_VT_"  << top_sigma_str[top_sigma] << wl_ss.str() << " " << eop_vt << endl;
				//}

				if (size_t size = eop_sig_all[top_sigma].size()) {
					sort(eop_sig_all[top_sigma].begin(), eop_sig_all[top_sigma].end());
					double eop_sig = size % 2 ? eop_sig_all[top_sigma][size / 2] : (eop_sig_all[top_sigma][size / 2] + eop_sig_all[top_sigma][size / 2 - 1]) / 2;
					os << eop_name << "_SIG_" << top_sigma_str[top_sigma] << wl_ss.str() << " " << eop_sig << std::endl;
				}
			}
		} // WL

		if (num_blocks) {
			sig_results.print(os, s);
			vt_med_results.print(os, s);
			pvs_ofst_results.print(os, s);
			pvs_pm3p5s_results.print(os, s);
		}

	} // dut
} // calc_sppspe