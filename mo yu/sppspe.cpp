void sppspe(const string& name, const block_list& blks, const init_mode& i)
{
	int wls[] = { 2, 29, 58, -1 };
	const int sppspe_subblock = 4;
	PageMap page_map = getPageMap(name.c_str());
	vector<uint64_t> pages;
	const double vpass_target = 12.0;

	// setup pages
	int num_wls = 0;
	for (int wli = 0; wls[wli] > 0; ++wli){
		++num_wls;
		pages.push_back(page_map.getPage(wls[wli], sppspe_subblock, LOWER_PAGE));
	}

	// setup hooks
	trim_map_sample_block_hook sppspe_hook;
	sppspe_hook.set(blks).add_overrides("PGMERS/q"); 
	//todo: add overrides???
	sppspe_hook.add_trim_shmoo_analog("R_TSS_EDGE_RBASE", -2.5, 6, 0.05);
	sppspe_hook.add_trim_shmoo_analog("R_TTX_LV4_RBASE", -2.5, 6, 0.05);
	// why tss edge and ttx lv4?
	sppspe_hook.add_scratch(pages, "page_list_start", "num_pages");
	int num_read_steps = sppspe_hook.num_shmoo_steps();
	
	std::stringstream sppspe_counts; sppspe_counts << "ERS_BITS/q " << num_wls << " SPP_BITS/q " << (num_wls * num_read_steps) << " SPE_BITS/q " <<(num_wls * num_read_steps);
	func_test(name.c_str(), "p_sppspe", sppspe_hook, 0, sppspe_counts.str().c_str(),0, ra_mode_none, 0)
	//todo: patspec "p_sppspe ..."
	
	// calc shmoo for ers,spp,spe
	calc_sppspe(name, sppspe_hook, wls, num_read_steps);

	// delete bits
	erase_count_result(name + ".*_BITS");
	print_actual_blks(name.c_str(), blks);
}