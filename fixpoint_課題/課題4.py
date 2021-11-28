import datetime

#N回以上連続のタイムアウトで故障判定
N = int(input("何回以上で故障にする？"))
#直近m回の平均応答時間計算
m = int(input("直近の応答時間の保存数"))
#tミリ秒を超えた場合サーバーが過負荷
t = int(input("過負荷状態は何ミリ秒から？"))
#IPアドレス: インスタンス
hist = {}
#IPアドレス: エラーかどうか
error_hist = {}
#テキストファイル
TEXT = "logfile4.txt"


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
        #過去５回までの履歴
        self.his_tm = []

    
    def setup(self):
        #応答回数を格納
        self.total_tm += 1
        self.his_tm.append(int(self.restm))
        #もし応答がエラーなら
        if self.restm == "-":
            #連続エラー回数を増やし
            self.timeout_tm += 1

            
    def update(self, tm):
        #応答回数を格納
        self.total_tm += 1
        #もし応答がエラーなら
        if tm == "-":
            #連続エラー回数を増やし
            self.timeout_tm += 1
            #もし初めてのエラーなら
            if self.timeout_tm == 1:
                #エラーの時間を格納
                self.timeout_date = self.date
                print("初めてのエラー")
        #応答がエラー出ないならリセット
    
    #２回目以降タイムアウト判定後タイムアウト時間
    def break_time(self, tm, date):
        #連続エラーが起きている場合
        if self.timeout_tm > 0:
            #今回もエラーならいったんそのまま
            if tm == '-':
                print("エラー中")
            # #今回復活したら復活するまでにかかった時間を返す
            else:
                if N <= self.timeout_tm:
                    self.timeout_tm = 0
                    return datetime.datetime.strptime(str(date), '%Y%m%d%H%M%S') - datetime.datetime.strptime(str(self.timeout_date), '%Y%m%d%H%M%S')
                else:
                    print("エラーの様子見")
    
    #過負荷のチェック
    def over_check(self, tm, date):
        #平均値
        mean = 0
        #履歴が５個ある場合は一番古いデータの削除
        if len(self.his_tm) == m:
            self.his_tm.pop(0)
        self.his_tm.append(int(tm)) if tm != "-" else print("エラーのためデータなし")
        if len(self.his_tm):
            mean = sum(self.his_tm)/len(self.his_tm)
        #過負荷の判定
        if mean > t:
            print("過負荷です: {}".format(datetime.datetime.strptime(str(date), '%Y%m%d%H%M%S')))
            # print(self.his_tm)
            return True

#引数にクラス格納予定の値を扱い、初めてのアドレスかそうでないかの判定

def judge(date, mask, ads, restm):
    if ads in hist:
        print("既出のアドレス", ads)
        error(mask, ads, restm)
        hist[ads].update(restm)
        hist[ads].over_check(restm, date)
        i = hist[ads].break_time(restm, date)
        print("エラー時間: {}".format(i)) if i else print("出力なし")
        
    else:
        print("初めてのアドレス", ads)
        #エラーhistとhistにデータを格納
        error(mask, ads, restm)
        hist[ads] = subnet(date, mask, ads, restm)
        hist[ads].setup()
        hist[ads].over_check(restm, date)
        i = hist[ads].break_time(restm, date)
        print("エラー時間: {}".format(i)) if i else print("出力なし")
        
def error(mask, ads, restm):
    #綺麗なIPアドレス
    address = ""
    for ad in ads.split("."):
        address += str(ad.zfill(3))
    address = address[:mask*3//8]
    if address in error_hist:
        pass
    else:
        #エラーしていない:0
        error_hist[address] = 0
    #エラーかどうか
    error_hist[address] = error_hist[address]+1 if restm == "-" else 0
    if error_hist[address] >= N:
        print("サブネットスイッチが故障: {}".format(address)) 

def main():
    f = open(TEXT, 'r')
    datalist = f.readlines()
    f.close()

    for data in datalist:
        dat = data.split(",")
        date = int(dat[0])
        # ads = dat[1].split("/")[0].replace(".", "")
        ads = dat[1].split("/")[0]
        address = ""
        for ad in ads.split("."):
            address += str(ad.zfill(3))
        # adress = dat[1].split("/")[0]
        mask = int(dat[1].split("/")[1])
        restm = dat[2].split()[0]
    #     print(restm)
        judge(date, mask, address, restm)
        print("----------------------------------------------------------------")
    # print(error_hist)

if __name__ == "__main__":
    # execute only if run as a script
    main()