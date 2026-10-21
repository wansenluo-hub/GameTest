const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');

const out = 'E:/微信公众号/accounts-data/ai-anli/图片/封面/009-Claude被薅了2880万次-v3.png';

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
      background: #efe8d8;
      color: #141414;
    }
    .cover {
      position: relative;
      width: 900px;
      height: 382px;
      overflow: hidden;
      background:
        linear-gradient(90deg, rgba(0,0,0,.04) 1px, transparent 1px),
        linear-gradient(rgba(0,0,0,.04) 1px, transparent 1px),
        radial-gradient(circle at 70% 20%, rgba(190, 38, 38, .16), transparent 28%),
        #efe8d8;
      background-size: 28px 28px, 28px 28px, auto, auto;
    }
    .paper {
      position: absolute;
      left: 46px;
      top: 34px;
      width: 360px;
      height: 292px;
      background: #fbf7ec;
      border: 2px solid #1d1d1d;
      box-shadow: 12px 12px 0 rgba(0,0,0,.16);
      transform: rotate(-3deg);
      padding: 24px 24px;
    }
    .paper::before {
      content: "CONFIDENTIAL";
      position: absolute;
      right: 18px;
      top: 18px;
      color: rgba(173, 28, 28, .24);
      font-size: 34px;
      font-weight: 900;
      transform: rotate(8deg);
    }
    .paper-title {
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 0;
      border-bottom: 4px solid #141414;
      padding-bottom: 10px;
      width: 210px;
    }
    .claude-box {
      margin-top: 28px;
      width: 180px;
      height: 88px;
      border: 3px solid #141414;
      display: grid;
      place-items: center;
      font-size: 34px;
      font-weight: 900;
      background: #ffffff;
    }
    .question {
      position: absolute;
      left: 240px;
      top: 102px;
      width: 78px;
      height: 78px;
      border-radius: 50%;
      border: 5px solid #b91c1c;
      color: #b91c1c;
      display: grid;
      place-items: center;
      font-size: 58px;
      font-weight: 900;
      transform: rotate(10deg);
      background: #fbf7ec;
    }
    .stamp {
      position: absolute;
      left: 196px;
      bottom: 34px;
      border: 5px solid #b91c1c;
      color: #b91c1c;
      font-size: 33px;
      font-weight: 900;
      padding: 8px 18px;
      transform: rotate(-10deg);
      opacity: .92;
    }
    .cards {
      position: absolute;
      left: 330px;
      top: 42px;
      width: 250px;
      height: 286px;
    }
    .id {
      position: absolute;
      width: 116px;
      height: 74px;
      background: #fff;
      border: 2px solid #141414;
      box-shadow: 6px 6px 0 rgba(0,0,0,.13);
      padding: 9px;
    }
    .id::before {
      content: "";
      display: block;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: #222;
      margin-bottom: 8px;
    }
    .id::after {
      content: "";
      display: block;
      width: 72px;
      height: 8px;
      background: #d7d0c1;
      box-shadow: 0 14px 0 #d7d0c1;
      position: absolute;
      right: 10px;
      top: 15px;
    }
    .id:nth-child(1) { left: 8px; top: 14px; transform: rotate(8deg); }
    .id:nth-child(2) { left: 94px; top: 72px; transform: rotate(-7deg); }
    .id:nth-child(3) { left: 28px; top: 150px; transform: rotate(5deg); }
    .id:nth-child(4) { left: 122px; top: 198px; transform: rotate(9deg); }
    .redline {
      position: absolute;
      height: 3px;
      background: #b91c1c;
      transform-origin: left center;
      opacity: .9;
    }
    .l1 { left: 360px; top: 88px; width: 180px; transform: rotate(20deg); }
    .l2 { left: 434px; top: 132px; width: 136px; transform: rotate(2deg); }
    .l3 { left: 386px; top: 208px; width: 190px; transform: rotate(-17deg); }
    .l4 { left: 478px; top: 252px; width: 118px; transform: rotate(-38deg); }
    .headline {
      position: absolute;
      right: 44px;
      top: 46px;
      width: 385px;
    }
    .kicker {
      display: inline-block;
      padding: 7px 12px;
      background: #141414;
      color: #fff;
      font-size: 20px;
      font-weight: 800;
      letter-spacing: 0;
    }
    h1 {
      margin: 18px 0 0;
      font-size: 58px;
      line-height: 1.04;
      font-weight: 900;
      letter-spacing: 0;
    }
    h1 .red {
      color: #b91c1c;
    }
    .sub {
      margin-top: 16px;
      font-size: 25px;
      line-height: 1.28;
      font-weight: 700;
      color: #333;
    }
    .number {
      position: absolute;
      right: 54px;
      bottom: 42px;
      display: flex;
      gap: 12px;
      align-items: baseline;
      padding: 10px 16px;
      background: #fff;
      border: 3px solid #141414;
      box-shadow: 7px 7px 0 rgba(0,0,0,.16);
    }
    .number strong {
      color: #b91c1c;
      font-size: 38px;
      font-weight: 900;
    }
    .number span {
      font-size: 22px;
      font-weight: 900;
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="paper">
      <div class="paper-title">AI CASE FILE</div>
      <div class="claude-box">Claude</div>
      <div class="question">?</div>
      <div class="stamp">被偷师?</div>
    </div>
    <div class="cards">
      <div class="id"></div>
      <div class="id"></div>
      <div class="id"></div>
      <div class="id"></div>
    </div>
    <div class="redline l1"></div>
    <div class="redline l2"></div>
    <div class="redline l3"></div>
    <div class="redline l4"></div>
    <div class="headline">
      <div class="kicker">AI 圈调查</div>
      <h1>Claude<br>被<span class="red">薅</span>出<br>一场风波</h1>
      <div class="sub">大模型最贵的能力，正在被复制</div>
    </div>
    <div class="number"><strong>2880万</strong><span>次交互</span></div>
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
