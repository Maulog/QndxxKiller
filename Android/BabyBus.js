auto.waitFor();//检查是否配置无障碍模式
var now = new Date();
if(now.getDay()!=1)hamibot.exit();//星期几执行

console.show();
console.log('欢迎来到宝宝巴士！');

/**
 * @description: 获取手机当前信息函数
 * @param: null
 * @return: null
 */
function Init(){
  while(screenLockedStatus());
  log("脚本开始运行");
	console.log('当前手机的安卓版本为',device.release);
	console.log('目前手机的电量为',device.getBattery(),'%');
  console.log('手机的分辨率为',device.width,'x',device.height);
  setScreenMetrics(1080,2340);
  if (!requestScreenCapture()) {
    console.log('没有授予 Hamibot 屏幕截图权限');
    hamibot.exit();
  }
}

/**
 * @description: 获取手机锁屏状态函数
 * @param: null
 * @return: 锁屏状态
 */
function screenLockedStatus(){
    importClass(android.app.KeyguardManager)
    importClass(android.content.Context)
    var km = context.getSystemService(Context.KEYGUARD_SERVICE);
    // ture-锁屏， false-已解锁
    return km.isKeyguardLocked();
}

/**
 * @description: 关闭应用函数
 * @param: null
 * @return: null
 */
function killApp(name) {
    var packageName = app.getPackageName(name);
    app.openAppSetting(packageName);
    sleep(1000);
    while (true) {
      if (text("结束运行").exists()) {
        click("结束运行");
        sleep(500);
        while (true) {
          if (text("确定").exists()) {
            click("确定");
            sleep(500);
            break;
          }
        }
        break;
      } else if (text("强行停止").exists()) {
        click("强行停止");
        sleep(500);
        while (true) {
          if (text("确定").exists()) {
            click("确定");
            sleep(500);
            break;
          }
          else if (text("强行停止").exists()) {
            click("强行停止");
            sleep(500);
            break;
          }
        }
        break;
      }
    }
    back();
    home();
    sleep(2000);
	}

/**
 * @description: 一键青年大学习
 * @param: null
 * @return: null
 */
function teenStudy(){
  sleep(2000);
  files.ensureDir('./Hemibot/babybus/');
	launchApp("微信");
  sleep(2000);
  killApp("微信");
  launchApp("微信");
	sleep(600);
  while(!desc("搜索").exists());//等待加载完毕
  var searchButton=desc("搜索").findOne();
  searchButton.click();
  while(!desc("取消按钮").exists());
  setText("辽宁共青团");
  sleep(3500);//搜索时间
  var GQT=className("android.widget.RelativeLayout").indexInParent(2).findOne();
  GQT.click();
  sleep(2000);
  
  //此处不同省份不一样
  var QXX1=className("android.widget.FrameLayout").drawingOrder(2).clickable(true).findOne();
  QXX1.click();
  sleep(4800);
  while(!click('青学习'));
  sleep(2000);
  
  //接下来是选择某一期（待修改）
  var DXX=className("android.view.View").indexInParent(1).clickable(true).findOne();
  DXX.click();
  sleep(3000);
  /////////
  
  if(text("--请选择--").enabled(true).exists()){
    var Province=text("--请选择--").clickable(true).findOnce(0);
    Province.click();
    while(!click('辽宁省'));
    sleep(300);
    var City=text("--请选择--").clickable(true).findOnce(0);
    City.click();
    while(!click('大连市'));
    sleep(300);
    var OK1=className('android.view.View').clickable(true).findOne();
    OK1.click();
  }
  sleep(5000);
  
  function myCapScreen(){
  	console.hide();
    sleep(300);
    var image = captureScreen();
    console.show();
    return image;
  }
  
  var img = myCapScreen();
  var scrtxt = ocr.recognizeText(img);
  if(scrtxt.indexOf("我要签到")!=-1){
  	var OK2=className('android.view.View').clickable(true).enabled(true).findOne();
  	OK2.click();
    console.log("虽然出现了我要签到的界面，不过我帮你点了");
    sleep(4000);
  }else{
  	console.log("识别到的内容为：\n",scrtxt);

  }
  img.recycle();
  
  
  var OK3=className('android.view.View').clickable(true).enabled(true).findOne();
  OK3.click();
  console.log('开始自动大学习');
  sleep(30000);
  while(true){
    //判断条件:每隔3秒截屏如果出现了“确定”判断进入了习题，如果出现了“课后习题”或“恭喜你”跳出
    img = myCapScreen();
    scrtxt = ocr.recognizeText(img);
    if(scrtxt.indexOf("确定")!=-1){//此处点击的是控件（仅针对四个选项的选择题），如有更好的ocr可直接点击坐标
      console.log("发现题目");
      console.log("识别到的内容为：",scrtxt);
      click(534,1878);//点击确定
      sleep(4000);
      click(935,2105);//点击继续听讲
//       var OK=className('android.view.View').clickable(true).indexInParent(5).findOne();
//       OK.click();
//       var GOON=className('android.view.View').clickable(true).indexInParent(10).findOne();
//       GOON.click();
    }else if(scrtxt.indexOf("恭喜你")!=-1|scrtxt.indexOf("课后习题")!=-1){
    	console.log("学习完成");
      images.save(img,'./Hemibot/babybus/qndxx.png');
      console.log("保存学习截图在./Hemibot/babybus/qndxx.png");
      img.recycle();
      console.log("学习完成");
      break;
    }else{
    	console.log("识别到的内容为：",scrtxt);
    }
    img.recycle();
    sleep(4000);
  }
	for(var i=0;i<5;i++){
  	back();
    sleep(700);
  };
  home();
  console.log("退出脚本");
}
Init();
teenStudy();

hamibot.exit();








