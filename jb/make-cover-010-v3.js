const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');

const out = 'E:/微信公众号/accounts-data/ai-anli/图片/封面/010-AI大厂准备退路-v3.png';

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
      background: #08111f;
      color: #fff;
    }
    .cover {
      position: relative;
      width: 900px;
      height: 382px;
      overflow: hidden;
      background:
        radial-gradient(circle at 28% 36%, rgba(0, 220, 255, .28), transparent 28%),
        radial-gradient(circle at 74% 44%, rgba(255, 185, 65, .24), transparent 26%),
        linear-gradient(135deg, #06111e 0%, #0b1730 50%, #101728 100%);
    }
    .grid {
      position: absolute;
      inset: 0;
      opacity: .18;
      background-image:
        linear-gradient(rgba(255,255,255,.12) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.12) 1px, transparent 1px);
      background-size: 36px 36px;
    }
    .stage {
      position: absolute;
      left: 42px;
      top: 54px;
      width: 382px;
      height: 248px;
      border: 1px solid rgba(110, 235, 255, .42);
      background: rgba(255,255,255,.06);
      box-shadow: 0 0 34px rgba(0,220,255,.16);
      overflow: hidden;
    }
    .desk {
      position: absolute;
      left: 36px;
      bottom: 46px;
      width: 280px;
      height: 22px;
      background: #2b3950;
      border-radius: 14px;
    }
    .screen {
      position: absolute;
      left: 210px;
      top: 64px;
      width: 95px;
      height: 72px;
      border: 3px solid #6eebff;
      background: rgba(0,220,255,.12);
      box-shadow: 0 0 20px rgba(110,235,255,.35);
    }
    .screen::before, .screen::after {
      content: "";
      position: absolute;
      left: 14px;
      right: 14px;
      height: 6px;
      background: rgba(255,255,255,.7);
      border-radius: 4px;
    }
    .screen::before { top: 18px; }
    .screen::after { top: 38px; width: 42px; }
    .bot {
      position: absolute;
      left: 72px;
      top: 62px;
      width: 110px;
      height: 104px;
      border-radius: 28px;
      border: 3px solid #6eebff;
      background: linear-gradient(180deg, rgba(110,235,255,.24), rgba(110,235,255,.08));
      box-shadow: 0 0 28px rgba(110,235,255,.28);
    }
    .bot::before {
      content: "";
      position: absolute;
      left: 26px;
      top: 30px;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #fff;
      box-shadow: 44px 0 0 #fff;
    }
    .bot::after {
      content: "AI";
      position: absolute;
      left: 0;
      right: 0;
      bottom: 18px;
      text-align: center;
      font-size: 32px;
      font-weight: 900;
      color: #6eebff;
    }
    .arrow {
      position: absolute;
      left: 180px;
      top: 110px;
      width: 80px;
      height: 4px;
      background: #ffcf5a;
      box-shadow: 0 0 16px rgba(255,207,90,.55);
    }
    .arrow::after {
      content: "";
      position: absolute;
      right: -2px;
      top: -8px;
      border-left: 16px solid #ffcf5a;
      border-top: 10px solid transparent;
      border-bottom: 10px solid transparent;
    }
    .road {
      position: absolute;
      right: 52px;
      top: 78px;
      width: 300px;
      height: 222px;
    }
    .road-line {
      position: absolute;
      left: 30px;
      top: 22px;
      width: 190px;
      height: 146px;
      border: 7px solid #ffcf5a;
      border-left: 0;
      border-bottom: 0;
      border-radius: 0 80px 0 0;
      transform: rotate(-8deg);
      filter: drop-shadow(0 0 12px rgba(255,207,90,.34));
    }
    .sign {
      position: absolute;
      right: 0;
      top: 0;
      width: 186px;
      height: 92px;
      background: #ffcf5a;
      color: #111827;
      border-radius: 8px;
      display: grid;
      place-items: center;
      text-align: center;
      font-size: 30px;
      line-height: 1.12;
      font-weight: 900;
      box-shadow: 8px 8px 0 rgba(0,0,0,.22);
    }
    .person {
      position: absolute;
      left: 14px;
      bottom: 8px;
      width: 84px;
      height: 138px;
    }
    .head {
      width: 42px;
      height: 42px;
      margin: 0 auto;
      border-radius: 50%;
      background: #fff;
      box-shadow: 0 0 0 4px rgba(255,255,255,.16);
    }
    .body {
      width: 70px;
      height: 80px;
      margin: 8px auto 0;
      border-radius: 24px 24px 10px 10px;
      background: #dbeafe;
    }
    .bag {
      position: absolute;
      right: 0;
      bottom: 34px;
      width: 34px;
      height: 44px;
      border-radius: 7px;
      background: #ff5358;
    }
    .headline {
      position: absolute;
      left: 44px;
      bottom: 28px;
      right: 44px;
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 24px;
    }
    h1 {
      margin: 0;
      width: 530px;
      font-size: 54px;
      line-height: 1.06;
      font-weight: 900;
      letter-spacing: 0;
    }
    h1 span { color: #6eebff; }
    .badge {
      flex: 0 0 auto;
      padding: 12px 18px;
      border: 1px solid rgba(255,255,255,.26);
      background: rgba(255,255,255,.1);
      color: #ffcf5a;
      font-size: 26px;
      font-weight: 900;
      backdrop-filter: blur(8px);
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="grid"></div>
    <div class="stage">
      <div class="bot"></div>
      <div class="arrow"></div>
      <div class="screen"></div>
      <div class="desk"></div>
    </div>
    <div class="road">
      <div class="person"><div class="head"></div><div class="body"></div><div class="bag"></div></div>
      <div class="road-line"></div>
      <div class="sign">退路<br>准备中</div>
    </div>
    <div class="headline">
      <h1>AI 替人干活，<br><span>大厂开始留后路</span></h1>
      <div class="badge">5 亿美元预案</div>
    </div>
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
