# main class

class Game:
    def __init__(self):
        self.gameboard = {}
        msg = "Welcome to droplets game."
        print(msg)
    def main(self):
        while True:
            print("main")


# drops at grids
class Drop:
    def __init__(self,x,y,size):
        self.x = x
        self.y = y
        self.size = size

    def __str__(self):
        return f"({self.x},{self.y}){self.size}"

    def add_water(self):
        self.size += 1
        if self.size > 9:
            self.size = 0
            # TODO: splash to four directions; if no drop in any direction, splash would bounce and diminish on the boarder.

        # 被迫绑定 - 
        # 女主每次进副本必带奶妈。
        # 副本可以带人，有人会选择带一个伙伴弥补短板。
        # 多数人猜测她的能力是残血加伤，自愈力差，所以随身携带奶妈。
        # 她不是残血加伤，而是没有参与资格。
        # 她是一个普通人，只有作为能力者的附带人才能进副本。
        # 领主永生被禁锢在主神空间里，但可以用幻境把别人的精神力收入领域。
        # 女主是上一任领主的囚犯，新上任的领主欣赏她，给了她一个活下去的选择。
        # 新领主有时候会把一些将死之人坑进空间，男主就是其中一个。
        # 女主非常娇小，身高只有一米五，抗造耐磨，恢复力极强，永远卡在要死不死的极限上暴力输出。
        # 男主——是个社畜。非常倒霉地被主神使唤，为主神鞍前马后。女主是给男主当保镖。

        # 对比：

        # 对女主：
        # 一时话不投机，她已经拿着睡袋睡下了。
        # 过了一会，他轻轻走过去，把睡袋放在她旁边，躺上之后又悄咪咪往她那蹭了蹭。
        # 火光被他的身影扰乱，映得她的侧脸一时莹润一时苍白。
        # 对女配：
        # 他有一搭没一搭地戳着火堆，抱着水瓶喝了两口。她拖着右手，盯着火光发呆。
        # 呆在这里不是办法。他挑了挑火堆，将手里的树枝丢进去，拿出怀里的水抿了一口。
        # 也没什么保暖的东西，还好身上穿得多。他裹了裹自己的外套，在火堆旁找了个平坦的地方，凑合着躺下了。
        
        # 对女主：
        # 女主完全不回答他的问题，转移话题，他思路马上跟着女主走。之前说的啥，不重要。
        # 对女配
        # 女配说着眼下的情况，然后抛出了一个有关女主的隐情，男主心里一点波澜都没有，纯当没听到。
        # 这人一看就不是什么好人，张口就要挑拨离间，听她说个鬼呦。
        # 
        # 
        # 
        # 他对她的执念，就是从这一秒开始的。