import datetime

class subnet:    
    def __init__(self, date, mask, ads, restm):
        #確認日時の時間への変更
        self.date = date
        #サブネットマスクの部分
        self.mask = mask
        #IPアドレスの部分
        self.ads = ads
        #pingの応答時間
        self.restm = restm
        #総出力数
        self.total_tm = 0
        #タイムアウト連続回数
        self.timeout_tm = 0
        #前回タイムアウト時点の時間の格納
        self.timeout_date = ""

    
    def setup(self):
        #応答回数を格納
        self.total_tm += 1
        #もし応答がエラーなら
        if self.restm == "-":
            #連続エラー回数を増やし
            self.timeout_tm += 1

            
    def update(self, tm):
        #応答回数を格納
        self.total_tm += 1
        #もし応答がエラーなら
        # print("アップデート", tm)
        if tm == "-":
            #連続エラー回数を増やし
            self.timeout_tm += 1
            #もし初めてのエラーなら
            if self.timeout_tm == 1:
                #エラーの時間を格納
                self.timeout_date = self.date
                print("初めてのエラー")
        #応答がエラー出ないならリセット
        # else:
            # print("連続エラーのリセット", tm)
    
    #２回目以降タイムアウト判定後タイムアウト時間
    def break_time(self, tm, date):
        #連続エラーが起きている場合
        if self.timeout_tm > 0:
            #今回もエラーならいったんそのまま
            if tm == '-':
                # print("エラー中", self.timeout_tm)
                return False
            #今回復活したら復活するまでにかかった時間を返す
            else:
                self.timeout_tm = 0
                # print("エラーからの復活", self.timeout_tm)
                return datetime.datetime.strptime(str(date), '%Y%m%d%H%M%S') - datetime.datetime.strptime(str(self.timeout_date), '%Y%m%d%H%M%S')
        else:
            # print("エラーなし")
            return False

#引数にクラス格納予定の値を扱い、初めてのアドレスかそうでないかの判定
hist = {}
def judge(date, mask, ads, restm):
    if ads in hist:
        print("既出のアドレス", ads)
        hist[ads].update(restm)
        i = hist[ads].break_time(restm, date)
        print("エラー時間: {}".format(i)) if i else print("エラーなし")
    else:
        print("初めてのアドレス", ads)
        hist[ads] = subnet(date, mask, ads, restm)
        hist[ads].setup()
        i = hist[ads].break_time(restm, date)
        print("エラー時間: {}".format(i)) if i else print("エラーなし")

def main():
    #テキストファイル
    TEXT = "logfile.txt"

    f = open(TEXT, 'r')
    datalist = f.readlines()
    f.close()

    for data in datalist:
        dat = data.split(",")
        date = int(dat[0])
        ads = dat[1].split("/")[0].replace(".", "")
        mask = int(dat[1].split("/")[1])
        restm = dat[2].split()[0]
    #     print(restm)
        judge(date, mask, ads, restm)

if __name__ == "__main__":
    # execute only if run as a script
    main()