const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');

const out = 'E:/微信公众号/accounts-data/ai-anli/图片/封面/010-AI大厂准备退路-v2.png';

function html() {
  return `<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      width: 900px;
      height: 382px;
      font-family: "Microsoft YaHei", "PingFang SC", Arial, sans-serif;
      background: #f7fbff;
      color: #102033;
    }
    .cover {
      position: relative;
      width: 900px;
      height: 382px;
      overflow: hidden;
      background:
        linear-gradient(135deg, #f7fbff 0%, #eef8ff 48%, #fff7e8 100%);
    }
    .panel {
      position: absolute;
      top: 34px;
      bottom: 34px;
      width: 388px;
      border: 3px solid #102033;
      background: #fff;
      box-shadow: 10px 10px 0 rgba(16,32,51,.14);
    }
    .left { left: 38px; }
    .right { right: 38px; }
    .split {
      position: absolute;
      left: 430px;
      top: 0;
      width: 40px;
      height: 382px;
      background: repeating-linear-gradient(
        45deg,
        #102033 0,
        #102033 10px,
        #ffd166 10px,
        #ffd166 20px
      );
      transform: skewX(-8deg);
      box-shadow: 0 0 0 3px #102033;
    }
    .tag {
      position: absolute;
      top: 24px;
      left: 24px;
      padding: 7px 13px;
      background: #00bcd4;
      color: #fff;
      font-size: 20px;
      font-weight: 900;
      border: 2px solid #102033;
    }
    .robot {
      position: absolute;
      left: 62px;
      top: 92px;
      width: 150px;
      height: 130px;
      border: 4px solid #102033;
      border-radius: 28px;
      background: #d9f7ff;
      box-shadow: inset 0 -12px 0 rgba(0,188,212,.18);
    }
    .robot::before {
      content: "";
      position: absolute;
      left: 28px;
      top: 34px;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      background: #102033;
      box-shadow: 70px 0 0 #102033;
    }
    .robot::after {
      content: "AI";
      position: absolute;
      left: 0;
      right: 0;
      bottom: 22px;
      text-align: center;
      font-size: 38px;
      font-weight: 900;
      color: #102033;
    }
    .arm {
      position: absolute;
      left: 210px;
      top: 145px;
      width: 94px;
      height: 16px;
      background: #102033;
      transform: rotate(-10deg);
      border-radius: 12px;
    }
    .task {
      position: absolute;
      right: 36px;
      top: 94px;
      width: 120px;
      height: 156px;
      background: #fff;
      border: 3px solid #102033;
      padding: 16px 12px;
      box-shadow: 7px 7px 0 rgba(16,32,51,.16);
    }
    .task div {
      height: 12px;
      background: #d8e1ea;
      margin-bottom: 14px;
    }
    .task div:nth-child(2) { width: 76px; }
    .task div:nth-child(3) { width: 92px; }
    .task div:nth-child(4) { width: 58px; }
    .left-title {
      position: absolute;
      left: 28px;
      bottom: 28px;
      font-size: 36px;
      line-height: 1.1;
      font-weight: 900;
    }
    .left-title span { color: #e63946; }
    .worker {
      position: absolute;
      left: 50px;
      top: 88px;
      width: 112px;
      height: 146px;
    }
    .head {
      width: 54px;
      height: 54px;
      border: 4px solid #102033;
      border-radius: 50%;
      background: #ffd166;
      margin: 0 auto;
    }
    .body {
      margin: 8px auto 0;
      width: 88px;
      height: 78px;
      border: 4px solid #102033;
      border-radius: 22px 22px 8px 8px;
      background: #ffefb0;
    }
    .map {
      position: absolute;
      right: 30px;
      top: 76px;
      width: 188px;
      height: 175px;
      background: #fff;
      border: 3px solid #102033;
      transform: rotate(4deg);
      box-shadow: 7px 7px 0 rgba(16,32,51,.16);
      padding: 16px;
    }
    .map h3 {
      margin: 0 0 12px;
      font-size: 24px;
      line-height: 1;
      color: #e63946;
    }
    .route {
      position: relative;
      height: 104px;
      border-left: 4px dashed #00bcd4;
      margin-left: 20px;
    }
    .route span {
      position: absolute;
      left: 18px;
      font-size: 20px;
      font-weight: 800;
      white-space: nowrap;
    }
    .route span:nth-child(1) { top: -4px; }
    .route span:nth-child(2) { top: 38px; }
    .route span:nth-child(3) { top: 80px; }
    .right-title {
      position: absolute;
      left: 28px;
      bottom: 28px;
      font-size: 36px;
      line-height: 1.1;
      font-weight: 900;
    }
    .right-title span { color: #00a6c7; }
    .headline {
      position: absolute;
      left: 238px;
      top: 18px;
      right: 238px;
      z-index: 4;
      text-align: center;
    }
    .headline .money {
      display: inline-block;
      padding: 8px 14px;
      background: #e63946;
      color: #fff;
      border: 3px solid #102033;
      box-shadow: 5px 5px 0 rgba(16,32,51,.18);
      font-size: 28px;
      font-weight: 900;
    }
    .main {
      position: absolute;
      left: 206px;
      right: 206px;
      bottom: 22px;
      z-index: 5;
      text-align: center;
      font-size: 44px;
      line-height: 1.08;
      font-weight: 900;
      color: #102033;
      text-shadow: 0 3px 0 #fff;
    }
    .main span { color: #e63946; }
  </style>
</head>
<body>
  <div class="cover">
    <div class="panel left">
      <div class="tag">AI 替人干活</div>
      <div class="robot"></div>
      <div class="arm"></div>
      <div class="task"><div></div><div></div><div></div><div></div></div>
      <div class="left-title">工作被<span>拆分</span><br>重新定价</div>
    </div>
    <div class="panel right">
      <div class="tag" style="background:#ffd166;color:#102033;">准备退路</div>
      <div class="worker"><div class="head"></div><div class="body"></div></div>
      <div class="map">
        <h3>退路地图</h3>
        <div class="route"><span>再培训</span><span>工资保险</span><span>职业导航</span></div>
      </div>
      <div class="right-title">大厂开始<br>给人<span>留后路</span></div>
    </div>
    <div class="split"></div>
    <div class="headline"><div class="money">5 亿美元预案</div></div>
    <div class="main">一边推 AI<br><span>一边准备退路</span></div>
  </div>
</body>
</html>`;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 900, height: 382 }, deviceScaleFactor: 2 });
  await page.setContent(html(), { waitUntil: 'load' });
  await page.screenshot({ path: out, type: 'png' });
  await browser.close();
  console.log(out);
})();
