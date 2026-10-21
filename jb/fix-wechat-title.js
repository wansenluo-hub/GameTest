const { chromium } = require('E:/微信公众号/工具/publisher/node_modules/playwright');
const cfg = require('E:/微信公众号/工具/publisher/config');

const title = 'Claude 被薅了 2880 万次，AI 圈最贵的秘密藏不住了';
const appmsgid = '100000051';

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

(async () => {
  const ctx = await chromium.launchPersistentContext(cfg.profileDir, cfg.launch);
  const page = ctx.pages()[0] || await ctx.newPage();
  await page.goto(cfg.mpHome, { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(cfg.pace.afterNav * 2);

  const token = (page.url().match(/token=(\d+)/) || [])[1];
  if (!token) throw new Error('没有检测到 token');

  const editUrl = `https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&type=77&appmsgid=${appmsgid}&token=${token}&lang=zh_CN`;
  await page.goto(editUrl, { waitUntil: 'domcontentloaded' }).catch(() => {});
  await page.waitForTimeout(cfg.pace.afterNav * 4);

  const titleOk = await page.evaluate((value) => {
    const el = document.querySelector('#title, textarea.js_article_title');
    if (!el) return false;
    el.value = value;
    el.dispatchEvent(new Event('input', { bubbles: true }));
    el.dispatchEvent(new Event('change', { bubbles: true }));
    el.dispatchEvent(new Event('blur', { bubbles: true }));
    return true;
  }, title);

  if (!titleOk) throw new Error('没有找到标题输入框');

  await page.waitForTimeout(cfg.pace.click);
  const saved = await clickByText(page, ['保存为草稿', '保存草稿', '保存']);
  await page.waitForTimeout(cfg.pace.afterNav * 2);

  console.log(JSON.stringify({
    saved,
    title,
    url: page.url(),
  }, null, 2));

  await ctx.close();
})().catch(async (error) => {
  console.error(error);
  process.exit(1);
});
