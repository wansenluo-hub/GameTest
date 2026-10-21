const path = require('path');
const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');

const out = 'E:/微信公众号/accounts-data/ai-anli/图片/封面/009-Claude被薅了2880万次-v2.png';

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
      color: #f8fbff;
      background: #080b12;
    }
    .cover {
      position: relative;
      width: 900px;
      height: 382px;
      overflow: hidden;
      background:
        radial-gradient(circle at 62% 45%, rgba(255, 83, 88, .22), transparent 24%),
        radial-gradient(circle at 18% 20%, rgba(77, 213, 255, .22), transparent 28%),
        linear-gradient(135deg, #111827 0%, #080b12 56%, #171b28 100%);
    }
    .matrix {
      position: absolute;
      inset: -40px;
      opacity: .12;
      background-image:
        linear-gradient(rgba(255,255,255,.16) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.16) 1px, transparent 1px);
      background-size: 34px 34px;
      transform: rotate(-7deg) scale(1.15);
    }
    .core {
      position: absolute;
      left: 72px;
      top: 78px;
      width: 255px;
      height: 210px;
      border: 2px solid rgba(92, 225, 255, .75);
      background:
        radial-gradient(circle at 50% 38%, rgba(92,225,255,.22), transparent 44%),
        rgba(7, 18, 28, .82);
      box-shadow: 0 0 36px rgba(92,225,255,.26), inset 0 0 28px rgba(92,225,255,.16);
      clip-path: polygon(8% 0, 92% 0, 100% 12%, 100% 88%, 92% 100%, 8% 100%, 0 88%, 0 12%);
    }
    .core::before {
      content: "";
      position: absolute;
      inset: 34px 48px 54px;
      border: 3px solid #5ce1ff;
      border-radius: 50% 50% 45% 45%;
      box-shadow: 0 0 28px rgba(92,225,255,.38);
    }
    .core::after {
      content: "Claude";
      position: absolute;
      left: 0;
      right: 0;
      bottom: 26px;
      text-align: center;
      font-size: 38px;
      font-weight: 800;
      letter-spacing: 0;
      color: #ffffff;
    }
    .lock {
      position: absolute;
      left: 154px;
      top: 147px;
      width: 62px;
      height: 48px;
      border: 3px solid #ffcf5a;
      border-radius: 8px;
      box-shadow: 0 0 18px rgba(255,207,90,.45);
    }
    .lock::before {
      content: "";
      position: absolute;
      left: 12px;
      top: -34px;
      width: 32px;
      height: 38px;
      border: 3px solid #ffcf5a;
      border-bottom: 0;
      border-radius: 24px 24px 0 0;
    }
    svg.lines {
      position: absolute;
      inset: 0;
      width: 900px;
      height: 382px;
    }
    .line {
      fill: none;
      stroke: #ff5358;
      stroke-width: 2.4;
      stroke-dasharray: 7 8;
      opacity: .82;
      filter: drop-shadow(0 0 5px rgba(255,83,88,.75));
    }
    .node {
      position: absolute;
      width: 58px;
      height: 58px;
      border-radius: 50%;
      border: 1px solid rgba(255,255,255,.28);
      background: rgba(255,255,255,.08);
      display: grid;
      place-items: center;
      color: rgba(255,255,255,.9);
      font-size: 22px;
      font-weight: 800;
      box-shadow: 0 0 18px rgba(255,83,88,.16);
    }
    .node::after {
      content: "";
      width: 18px;
      height: 18px;
      border-radius: 50%;
      border: 2px solid rgba(255,255,255,.72);
      border-bottom: 0;
      position: absolute;
      top: 12px;
    }
    .node::before {
      content: "";
      width: 29px;
      height: 15px;
      border-radius: 16px 16px 6px 6px;
      border: 2px solid rgba(255,255,255,.72);
      position: absolute;
      bottom: 12px;
    }
    .n1 { left: 410px; top: 50px; }
    .n2 { left: 515px; top: 118px; }
    .n3 { left: 430px; top: 236px; }
    .n4 { left: 625px; top: 58px; }
    .n5 { left: 688px; top: 210px; }
    .headline {
      position: absolute;
      right: 48px;
      top: 54px;
      width: 385px;
      z-index: 5;
    }
    .tag {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 12px;
      background: rgba(255,83,88,.18);
      border: 1px solid rgba(255,83,88,.55);
      color: #ffb7ba;
      font-size: 20px;
      font-weight: 700;
    }
    h1 {
      margin: 18px 0 0;
      font-size: 54px;
      line-height: 1.08;
      letter-spacing: 0;
      font-weight: 900;
    }
    h1 span { color: #5ce1ff; }
    .sub {
      margin-top: 16px;
      font-size: 24px;
      line-height: 1.35;
      color: rgba(255,255,255,.76);
    }
    .count {
      position: absolute;
      left: 64px;
      bottom: 42px;
      padding: 11px 16px;
      color: #ffcf5a;
      font-size: 28px;
      font-weight: 900;
      border: 1px solid rgba(255,207,90,.5);
      background: rgba(255,207,90,.08);
      box-shadow: 0 0 18px rgba(255,207,90,.16);
    }
  </style>
</head>
<body>
  <div class="cover">
    <div class="matrix"></div>
    <svg class="lines" viewBox="0 0 900 382">
      <path class="line" d="M440 79 C365 94, 340 116, 300 150" />
      <path class="line" d="M535 147 C440 154, 380 159, 304 168" />
      <path class="line" d="M456 265 C390 236, 348 218, 292 195" />
      <path class="line" d="M642 87 C510 110, 407 131, 309 155" />
      <path class="line" d="M699 235 C544 220, 419 202, 296 184" />
    </svg>
    <div class="core"></div>
    <div class="lock"></div>
    <div class="node n1"></div>
    <div class="node n2"></div>
    <div class="node n3"></div>
    <div class="node n4"></div>
    <div class="node n5"></div>
    <div class="headline">
      <div class="tag">模型蒸馏风波</div>
      <h1>Claude 被<span>薅</span>了<br>2880 万次</h1>
      <div class="sub">AI 圈最贵的秘密，藏不住了</div>
    </div>
    <div class="count">25,000 个虚假账号</div>
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
