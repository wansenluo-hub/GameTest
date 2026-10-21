const fs = require('fs');
const path = require('path');
const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');
const cfg = require('E:/微信公众号/工具/publisher/config');
const { injectTitle, injectAuthor } = require('E:/微信公众号/工具/publisher/inject');

const appmsgid = '100000057';
const title = '大厂一边让 AI 替人干活，一边开始给人准备退路';
const author = 'AI案例拆解';
const mdFile = 'E:/微信公众号/accounts-data/ai-anli/published/010-大厂一边让AI替人干活一边开始给人准备退路.md';
const outFile = 'E:/微信公众号/accounts-data/ai-anli/published/010-大厂一边让AI替人干活一边开始给人准备退路.magazine-dark.wx.html';

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function paragraph(text, options = {}) {
  const color = options.muted ? '#9fb1c9' : '#d9e3f1';
  const bg = options.bg || '#111a2b';
  const border = options.border || '1px solid rgba(91, 214, 255, .16)';
  return `<p style="margin:0 0 13px;padding:14px 15px;line-height:1.9;font-size:16px;color:${color};background:${bg};border:${border};border-radius:8px;text-align:justify;letter-spacing:0;">${escapeHtml(text)}</p>`;
}

function sectionTitle(label, sub) {
  return `<section style="margin:26px 0 14px;padding:0;">
    <section style="display:inline-block;padding:7px 12px;background:#34d399;color:#06111d;font-size:14px;font-weight:700;border-radius:4px;letter-spacing:0;">${escapeHtml(label)}</section>
    ${sub ? `<section style="margin-top:10px;font-size:18px;line-height:1.55;color:#f8fafc;font-weight:700;letter-spacing:0;">${escapeHtml(sub)}</section>` : ''}
  </section>`;
}

function quote(text) {
  return `<section style="margin:18px 0;padding:16px 16px 16px 18px;background:#172033;border-left:5px solid #fbbf24;border-radius:7px;color:#f8fafc;font-size:17px;line-height:1.85;font-weight:700;letter-spacing:0;">${escapeHtml(text)}</section>`;
}

function chip(text) {
  return `<span style="display:inline-block;margin:0 7px 8px 0;padding:6px 9px;background:rgba(52,211,153,.12);border:1px solid rgba(52,211,153,.32);border-radius:4px;color:#9ff3cf;font-size:13px;line-height:1.2;">${escapeHtml(text)}</span>`;
}

function buildHtml(md) {
  const lines = md.replace(/^\uFEFF/, '').split(/\r?\n/);
  const body = lines
    .filter((line) => line.trim() && !line.startsWith('# '))
    .map((line) => line.trim());

  const refsIndex = body.findIndex((line) => line === '参考来源：');
  const content = refsIndex >= 0 ? body.slice(0, refsIndex) : body;
  const refs = refsIndex >= 0 ? body.slice(refsIndex + 1).filter((line) => line.startsWith('- ')).map((line) => line.slice(2)) : [];

  const intro = content.slice(0, 5);
  const debate = content.slice(5, 12);
  const signal = content.slice(12, 21);
  const selfCheck = content.slice(21, 31);
  const examples = content.slice(31, 41);
  const ending = content.slice(41);

  return `<section style="max-width:677px;margin:0 auto;padding:18px 12px 28px;background:#07111f;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',Arial,sans-serif;letter-spacing:0;">
    <section style="margin:0 0 18px;padding:20px 18px;background:linear-gradient(135deg,#10233c 0%,#08111f 58%,#15202f 100%);border:1px solid rgba(91,214,255,.25);border-radius:8px;box-shadow:0 10px 28px rgba(0,0,0,.22);">
      <section style="margin-bottom:13px;">
        ${chip('AI 热点观察')}${chip('就业重组')}${chip('5 亿美元信号')}
      </section>
      <section style="font-size:24px;line-height:1.35;color:#ffffff;font-weight:800;letter-spacing:0;">大厂开始给人准备退路，这条新闻比模型发布更值得看</section>
      <section style="margin-top:12px;color:#a9bdd6;font-size:15px;line-height:1.8;">不是贩卖焦虑，也不是替谁洗白。它真正暴露的是：AI 已经从“工具升级”，走到“岗位重新定价”。</section>
    </section>

    ${intro.map((text, index) => index === 3 ? quote(text) : paragraph(text, { muted: index === 2 })).join('')}

    ${sectionTitle('01', '以前的讨论太粗了')}
    ${debate.map((text, index) => index === 3 || index === 6 ? quote(text) : paragraph(text)).join('')}

    ${sectionTitle('02', '为什么大厂要提前准备退路')}
    ${signal.map((text, index) => index === 0 || index === 4 ? quote(text) : paragraph(text)).join('')}

    ${sectionTitle('03', '普通人真正该问的问题')}
    ${selfCheck.map((text, index) => index === 1 || index === 7 ? quote(text) : paragraph(text)).join('')}

    ${sectionTitle('04', '哪些能力会变便宜，哪些会变贵')}
    ${examples.map((text, index) => index === 0 || index === 5 ? quote(text) : paragraph(text)).join('')}

    ${sectionTitle('05', '最后一句实话')}
    ${ending.map((text, index) => index === ending.length - 2 ? quote(text) : paragraph(text)).join('')}

    <section style="margin:26px 0 0;padding:16px;background:#0d1728;border:1px solid rgba(148,163,184,.22);border-radius:8px;">
      <section style="margin-bottom:10px;color:#f8fafc;font-size:15px;font-weight:700;">参考来源</section>
      ${refs.map((text) => `<p style="margin:8px 0;line-height:1.65;color:#9fb1c9;font-size:13px;">• ${escapeHtml(text)}</p>`).join('')}
    </section>
  </section>`;
}

async function clickByText(page, texts) {
  for (const text of texts) {
    const locator = page.locator(`button:has-text("${text}"), a:has-text("${text}")`).first();
    if (await locator.count()) {
      try {
        await locator.click({ timeout: 5000 });
        return true;
      } catch {}
    }
  }
  return false;
}

async function replaceBody(page, html) {
  const editor = await page.evaluateHandle(() => {
    const list = [...document.querySelectorAll('.ProseMirror[contenteditable="true"], .ProseMirror')];
    let best = null;
    let area = 0;
    for (const el of list) {
      const r = el.getBoundingClientRect();
      const currentArea = r.width * r.height;
      if (currentArea > area && r.width > 300 && r.height > 300) {
        best = el;
        area = currentArea;
      }
    }
    return best;
  });
  const el = editor.asElement();
  if (!el) return false;

  await page.evaluate(async (h) => {
    const blob = new Blob([h], { type: 'text/html' });
    const text = new Blob([h.replace(/<[^>]+>/g, '')], { type: 'text/plain' });
    await navigator.clipboard.write([
      new ClipboardItem({ 'text/html': blob, 'text/plain': text }),
    ]);
  }, html);

  await el.click();
  await page.waitForTimeout(300);
  await page.evaluate((node) => {
    node.focus();
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(node);
    selection.removeAllRanges();
    selection.addRange(range);
  }, el);
  await page.waitForTimeout(150);
  await page.keyboard.press('Delete');
  await page.waitForTimeout(250);
  await page.keyboard.press('Control+V');
  await page.waitForTimeout(1800);

  return await page.evaluate(() => {
    const list = [...document.querySelectorAll('.ProseMirror[contenteditable="true"], .ProseMirror')];
    let best = null;
    let area = 0;
    for (const el of list) {
      const r = el.getBoundingClientRect();
      const currentArea = r.width * r.height;
      if (currentArea > area && r.width > 300 && r.height > 300) {
        best = el;
        area = currentArea;
      }
    }
    const text = best?.innerText || '';
    return (text.match(/真正的问题不是/g) || []).length <= 1;
  });
}
async function main() {
  const md = fs.readFileSync(mdFile, 'utf8');
  const html = buildHtml(md);
  fs.writeFileSync(outFile, html, 'utf8');

  const ctx = await chromium.launchPersistentContext(cfg.profileDir, cfg.launch);
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: 'https://mp.weixin.qq.com' }).catch(() => {});
  const page = ctx.pages()[0] || await ctx.newPage();

  await page.goto(cfg.mpHome, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(cfg.pace.afterNav * 2);
  const token = (page.url().match(/token=(\d+)/) || [])[1];
  if (!token) throw new Error('No token detected; please log in to mp.weixin.qq.com first.');

  const editUrl = `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=77&appmsgid=${appmsgid}&token=${token}&lang=zh_CN`;
  await page.goto(editUrl, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await page.waitForTimeout(cfg.pace.afterNav * 4);

  if (!(await injectTitle(page, title))) throw new Error('Title input not found.');
  await injectAuthor(page, author);
  if (!(await replaceBody(page, html))) throw new Error('Body editor replacement failed or duplicate old content remains.');

  await page.waitForTimeout(cfg.pace.afterNav);
  const saved = await clickByText(page, ['保存为草稿', '保存草稿', '保存']);
  await page.waitForTimeout(cfg.pace.afterNav * 2);
  await page.screenshot({ path: path.join(cfg.shotDir, 'draft-010-magazine-dark-saved.png'), fullPage: true }).catch(() => {});

  console.log(JSON.stringify({ saved, appmsgid, title, outFile, url: page.url() }, null, 2));
  await ctx.close();
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
