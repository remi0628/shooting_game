# Shooting Ggame 
高校3年生の夏休み課題で作成したゲームです。制作年：2017


# ScreenShot  

## start /game over /clear  
<p float="left">
  <img width="200" alt="スタート画面" src="https://user-images.githubusercontent.com/16487150/87143512-2b69b700-c2e1-11ea-89f7-b7bfebdd9527.png">
  <img width="200" alt="ゲームオーバー画面" src="https://user-images.githubusercontent.com/16487150/87148336-2f99d280-c2e9-11ea-83b6-eb5a5b4155e5.png">
  <img width="200" alt="クリア画面" src="https://user-images.githubusercontent.com/16487150/87148518-7c7da900-c2e9-11ea-8090-d18d329d26c1.png">
</p>  

## Small Fry Enemies stage /Medium Boss stage
* 雑魚敵(左画像)  
　しかし数が多いので注意が必要です。  
　敵を倒すと青いアイテムを落とします。
* 中ボス(右画像)  
　攻撃時以外はプレイヤーからの攻撃を殻で跳ね返して通しません。  
　攻撃時には弱点が現れます。敵は弾を連射してくるので注意が必要です。

<p float="left">
<img width="300" alt="雑魚敵" src="https://user-images.githubusercontent.com/16487150/87147877-5c011f00-c2e8-11ea-8ccf-2da5c3814c16.png">
<img width="300" alt="中ボス" src="https://user-images.githubusercontent.com/16487150/87148091-b7331180-c2e8-11ea-9f71-449cdaa6fbc3.png">
</p>


## Boss stage  
* メインボス  
　側面からプレイヤーの方向に弾を打ちます。  
　時にはライフルの様な構造部分からランダムにビームを放ちます。  
　ライフルの内側からは3方向に弾を撃ち出します。  
　敵による弾幕には注意しましょう。  
　ボスのHPはデフォルトで20に設定されています。  

<p float="left">
<img width="300" alt="ボス" src="https://user-images.githubusercontent.com/16487150/87148281-185ae500-c2e9-11ea-90e8-cfe3f528ab5d.png">
<img width="300" alt="ボス" src="https://user-images.githubusercontent.com/16487150/87149771-d0898d00-c2eb-11ea-952f-a1f0758dcfee.png">
</p>    


# system
## Shot Mode
* 弾の撃ち方は2種類存在  
・「T」：ボタンを一度押すと一発の弾を発射する。  
・「R」：ボタンを押しっぱなしの時、自動で連射する。  
 一見撃ち方は「R」で良いように見えるがアイテムを獲得しないと非常に連射が遅い。  
 連射が強化された場合でも人によっては「T」の連打撃ちの方が早いかもしれません。


<p float="left">
<img width="33" alt="スクリーンショット 2020-12-04 15 46 08" src="https://user-images.githubusercontent.com/16487150/101131035-fa02d680-3647-11eb-81f7-fca3eaa87e31.png">
<img width="27" alt="スクリーンショット 2020-12-04 15 46 36" src="https://user-images.githubusercontent.com/16487150/101131038-fc653080-3647-11eb-9a57-b9a56d368bf9.png">
</p>


## Item
* 敵からアイテムを獲得
　敵を倒すと一定の確率で青くて丸いアイテムがドロップします。  
 これを獲得する事によって自機の性能が強化されます。強化内容は以下に記載。  
 

  <img width="86" alt="アイテム" src="https://user-images.githubusercontent.com/16487150/101131809-3daa1000-3649-11eb-9fda-cf5ef86e692b.png">


## Item Effect
* 敵を倒した際に落とす青いアイテムを獲得すると、自機から発射される弾の種類が変化し連射速度が上昇します  
・左の画像：初期状態  
・右の画像：青いアイテムを獲得し強化された状態  


<p float="left">
<img width="76" alt="スクリーンショット 2020-12-04 15 52 27" src="https://user-images.githubusercontent.com/16487150/101131585-e0ae5a00-3648-11eb-9acb-595079c39862.png">
<img width="77" alt="スクリーンショット 2020-12-04 15 51 08" src="https://user-images.githubusercontent.com/16487150/101131465-ae046180-3648-11eb-914b-bdd299aed54d.png">
bullet.

<img width="60" alt="" src="https://user-images.githubusercontent.com/16487150/101132833-00df1880-364b-11eb-96c6-fe43c950d83d.png">
<img width="45" alt="連射速度上昇" src="https://user-images.githubusercontent.com/16487150/101132834-02104580-364b-11eb-9516-14d846ddcb15.png">
speed.
</p>


## Gif  
<img width="500" alt="雑魚敵" src="https://user-images.githubusercontent.com/16487150/101129414-da1de380-3644-11eb-98f5-943f78f62b3b.gif">

<img width="500" alt="中ボス" src="https://user-images.githubusercontent.com/16487150/101129602-40a30180-3645-11eb-96de-82e84542a124.gif">

<img width="500" alt="ボス" src="https://user-images.githubusercontent.com/16487150/101130741-629d8380-3647-11eb-92f1-bd01d2cf35f3.gif">
