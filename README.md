# GainPIDゲイン

F3RCでモーターのPIDゲインを調整する用に作ったプログラムです．
モーターの速度，位置の目標値と現時点の値をリアルタイムでPCに表示します．(遅延がでかくてリアルタイムと言っていいかよくわかりませんが)

あと簡易的なシリアル通信用のクラス`class SerialCommunication`も書きました

## ゲインチューニングのやり方

1. runner/main.cppでゲインを設定
2. runnerをマイコンに入れる．
3. serialMonitor/encoderMonitor.pyをマイコンと接続した状態で実行(グラフが表示される)
4. マイコンでプログラム実行
5. グラフを見てゲイン考え直す
6. 1~5を繰り返す


## モニターの見方

1. 上のグラフが速度，下のグラフが位置
2. 黄色が目標値，青色が現時点の値

## 注意

PCの方にpython環境と，pythonライブラリのnumpy, matplotlib, pyserialを入れる必要があります．pipですぐ入ります

モニターの方はとても低クオリティです．あんまり信頼しないで

モニターの下にあるEntryとButtonはPIDゲインをその場で変更して再実行できるようにしようとした名残ですが，いまんとこ動きません

## class SerialCommunication

副産物です．シリアル通信ができます．簡易的なものですがもしかしたらリモコンとR1の通信に使うかもしれないので使い方を書いておきます．

```cpp
//数値2つがカンマ区切りで送られてくるので，それを足した値を返すプログラム

#include "serialCommunication"


//PCとの通信にしか使ってないので細かい設定をする機能はつけてない
//必要ならいつでもつけれる
SerialCommunication serial;


//1行送られてきた時に割り込みで実行される
void interrupt(string line){
    float a, b;
    //a,bを受け取る
    sscanf(line, "%f,%f", &a, &b); //'\n'は必要なし

    //a+bを送る
    char result[64];
    sprintf(result, "%f", a+b); //'\n'は必要なし
    serial.writeline(result);
}


int main(){
    serial.attach(interrupt); //&は必要なし
    while (true) {}
}
```


