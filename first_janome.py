from janome.tokenizer import Tokenizer
t = Tokenizer()
malist = t.tokenize("すもももももももものうち")
for n in malist:
    print(n)
