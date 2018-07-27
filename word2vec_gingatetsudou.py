from janome.tokenizer import Tokenizer
from gensim.models import word2vec
import re

# テキストデータをバイナリとして一時的に読み込む'rb'read binay
binarydata = open("gingatetsudono_yoru.txt",'rb').read()
#バイナリデータをデコードして、コンピュータのプログラムから読める形にする
# pythonは標準でutf-8をでデコードするので、明示的にshit_jisを指定
text = binarydata.decode('shift_jis')
# text = re.split(r'', text)[2]
text = re.split(r'\-{5,}',text)[2]
text = re.split(r'底本：',text)[0]
text = text.strip()

# 形態素解析を行う

# janomeを利用するために、Tokenizerの初期化の関数を呼ぶ
t = Tokenizer()

# 分かち書きをした結果を格納するためのリスト型の変数
results = []

# データを改行コードで区切ってリストに格納する(行ごとにデータを格納する)
# shift_jisにふくまれる改行コードは\r\n
lines = text.split("\r\n")

# print(lines)
for line in lines:
    s = line
    s = s.replace('|','') # |を消去　
    s = re.sub(r'《.+?》','',s) #ルビをとる　re.subで正規表現のsubstitute(置換)
    s = re.sub(r'[#.+?]','',s) #入力注をとる
    tokens = t.tokenize(s) # 上記で前処理をしたデータに形態素解析をする
    r = []
    for token in tokens: # それぞれの形態素に対して処理をかけていく
        if token.base_form == "*": #もしも言葉の品詞が基本形"*"（*ワイルドカードなんらかの品詞）だったら、
            w = token.surface # surfaceをセット
        else:
            w = token.base_form # そうでない場合には、base_formをセット
        ps = token.part_of_speech # 品詞情報part_of_speech（tokenizerで提供される変数名）をセット
        hinsi = ps.split(',')[0] #品詞情報の先頭を取得
        if hinsi in ['名詞','形容詞','動詞','記号']: # 品詞がこれらのものなら、
            r.append(w) # リストの末尾に追加する
    rl = (" ".join(r)).strip() # スペースで連結した文字列を作成 ループを抜けたあとに行う
    results.append(rl)

    # 得られた分かち書きの結果をモデルデータとして書き出して、その後、ベクトル化して処理をしていく

    # モデルファイルに書き出す
    wakachigaki_file = "gingatetudou.wakachi"
    with open(wakachigaki_file, 'w',encoding='utf-8') as fp: # 'w'の指定で書き込み可能　as fpでfp(ファイルポインタ)という名称で扱えるようにする
        fp.write("\n".join(results)) # 改行コードを入れて先ほどの結果を書き込んでいく。これで、unix形式のファイルにutf-8でデータが保存されていく

    # word2vecでえられた単語一覧データをベクトル化していく
    # 詳細 https://radimrehurek.com/gensim/models/word2vec.html
data = word2vec.LineSentence(wakachigaki_file)
model = word2vec.Word2Vec(data,size=200, window=10, hs=1, min_count=2, sg =1)
model.save('gingatetudou.model')
# print('Completed')


print(model.most_similar(positive=['カムパネルラ']))





