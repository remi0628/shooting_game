# shooting_game
高校3年生の夏休み課題で作成したゲームです。制作年：2017

(This is a game I made when I was in high school.)  
(Production time: 2017)

# ScreenShot  

### start /game over /clear  
<p float="left">
  <img width="200" alt="スタート画面" src="https://user-images.githubusercontent.com/16487150/87143512-2b69b700-c2e1-11ea-89f7-b7bfebdd9527.png">
  <img width="200" alt="ゲームオーバー画面" src="https://user-images.githubusercontent.com/16487150/87148336-2f99d280-c2e9-11ea-83b6-eb5a5b4155e5.png">
  <img width="200" alt="クリア画面" src="https://user-images.githubusercontent.com/16487150/87148518-7c7da900-c2e9-11ea-8090-d18d329d26c1.png">
</p>  

### Small Fry Enemies stage /Medium Boss stage
* 雑魚敵(左画像)  
　しかし数が多いので注意が必要です。  
　敵を倒すと青いアイテムを落とします。
* 中ボス(右画像)  
　攻撃時以外はプレイヤーからの攻撃を殻で跳ね返して通しません。  
　攻撃時には弱点が現れます。敵は弾を連射してくるので注意が必要です。

(・The enemies are small fry enemies. But be careful because they are many in number.)  
(　If you defeat the enemies, you'll get blue items.)    
(・It is a medium boss existence. Except when it attacks, it does not pass through the attack by bouncing bullets from the player with its shell.)  
(　When he attacks, it is a weak point, but be careful because the enemy fires a series of bullets.)  
<p float="left">
<img width="300" alt="雑魚敵" src="https://user-images.githubusercontent.com/16487150/87147877-5c011f00-c2e8-11ea-8ccf-2da5c3814c16.png">
<img width="300" alt="中ボス" src="https://user-images.githubusercontent.com/16487150/87148091-b7331180-c2e8-11ea-9f71-449cdaa6fbc3.png">
</p>


### Boss stage  
・メインボス  
　側面からプレイヤーの方向に弾を打ちます。  
　時にはライフルの様な構造部分からランダムにビームを放ちます。  
　ライフルの内側からは3方向に弾を撃ち出します。  
　敵による弾幕には注意しましょう。  
　ボスのHPはデフォルトで20に設定されています。  

(・This is the main boss. From the side, it shoots bullets in the direction of your ship.)  
(　A beam is randomly shot from a place like a rifle.)  
(　From the inside of the rifle, he shoots bullets in three directions.)  
(　Be careful of the barrage of bullets.)
(　The HP of BOSS is 20 by default.)  
<p float="left">
<img width="300" alt="ボス" src="https://user-images.githubusercontent.com/16487150/87148281-185ae500-c2e9-11ea-90e8-cfe3f528ab5d.png">
<img width="300" alt="ボス" src="https://user-images.githubusercontent.com/16487150/87149771-d0898d00-c2eb-11ea-952f-a1f0758dcfee.png">
</p>    


# system
## Shot Mode
・敵を倒した際に落とす青いアイテムを獲得すると、自機から発射される弾の種類が変化し連射速度が上昇します  
　左の画像：初期状態  
　右の画像：青いアイテムを獲得し強化された状態  

(* If you acquire a blue item dropped by an enemy, the type of bullets fired from your ship will change and your continuous firing speed will increase.)  
(　Image on the left : Initial state)  
(　image on the right: the enhanced state that earned the blue items)  

<p float="left">
<img width="76" alt="スクリーンショット 2020-12-04 15 52 27" src="https://user-images.githubusercontent.com/16487150/101131585-e0ae5a00-3648-11eb-9acb-595079c39862.png">
<img width="77" alt="スクリーンショット 2020-12-04 15 51 08" src="https://user-images.githubusercontent.com/16487150/101131465-ae046180-3648-11eb-914b-bdd299aed54d.png">
</p>

<p float="left">
<img width="200" alt="" src="https://user-images.githubusercontent.com/16487150/87150311-c025e200-c2ec-11ea-8bae-03ca8e3a1c6b.png">
<img width="200" alt="連射速度上昇" src="https://user-images.githubusercontent.com/16487150/87150418-f5cacb00-c2ec-11ea-81a3-f123526d65b2.png">
</p>


<img width="33" alt="スクリーンショット 2020-12-04 15 46 08" src="https://user-images.githubusercontent.com/16487150/101131035-fa02d680-3647-11eb-81f7-fca3eaa87e31.png">
<img width="27" alt="スクリーンショット 2020-12-04 15 46 36" src="https://user-images.githubusercontent.com/16487150/101131038-fc653080-3647-11eb-9a57-b9a56d368bf9.png">


## Item

<img width="86" alt="アイテム" src="https://user-images.githubusercontent.com/16487150/101131809-3daa1000-3649-11eb-9fda-cf5ef86e692b.png">


## Gif  
<img width="500" alt="雑魚敵" src="https://user-images.githubusercontent.com/16487150/101129414-da1de380-3644-11eb-98f5-943f78f62b3b.gif">

<img width="500" alt="中ボス" src="https://user-images.githubusercontent.com/16487150/101129602-40a30180-3645-11eb-96de-82e84542a124.gif">

<img width="500" alt="ボス" src="https://user-images.githubusercontent.com/16487150/101130741-629d8380-3647-11eb-92f1-bd01d2cf35f3.gif">
