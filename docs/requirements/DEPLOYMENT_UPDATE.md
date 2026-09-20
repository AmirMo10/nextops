# Current deployment amendment / اصلاحیهٔ چیدمان فعلی

Revision: 2026-09-20 — dedicated Zabbix server. Publication was requested by the owner after the VM recommendation. Status: documented proposal; no provisioning or target-access approval is implied.

## English

Read [ZABBIX_SERVER](../en/ZABBIX_SERVER.md) and [ZABBIX_SERVER_PLAN.json](ZABBIX_SERVER_PLAN.json) with the [active master prompt](NEXTOPS_MASTER_PROMPT.md). This is a narrow amendment to v3.0 sections 18 and 22, the old optional-lab examples and the startup/combined capacity profile. It does not replace the security, offline, original integration or acceptance requirements.

For the new local monitoring-server path, use `zabbix-server`: **4 vCPU, 16 GiB RAM, 200 GiB virtual disk**, with its own PostgreSQL, Zabbix frontend/API and Agent 2. It replaces the earlier 4-vCPU/8-GiB/100-GiB `zabbix-lab` recommendation; do not create both by default. Existing suitable authorized Zabbix installations should be inspected and reused, not overwritten.

The initial three NextOps VMs stay at 36 vCPU / 168 GiB RAM / 780 GiB VMDKs. With the dedicated Zabbix VM, the selected combined profile is **4 VMs / 40 vCPU / 184 GiB RAM / 980 GiB VMDKs**. Provisional ESXi swap adds 184 GiB, for **1164 GiB before other overhead**. NextOps-only phase counts remain 3, then 4 after DB separation, then 5 with remediation; inclusive counts become 4, 5 and 6. Pure NextOps totals in historical guides are not additional resources to add again.

Create or reuse the authorized Zabbix dependency before Stage 1C live reads, alongside the existing application/AI/connector sequence. It may be prepared alongside 1A/1B, but real target credentials reach the connector only after the identity/policy/audit foundation passes. No Linux SSH connector, advanced RAG, extra database VM or remediation is needed for the first Zabbix answer.

The LVM and retention proposals are specified in the guide. Keep the 3 TB project ceiling, DS-C aliases, offline restart/new-answer tests, independent backups and exact-action controls. General local Q&A must remain possible when Zabbix is unreachable; current monitoring evidence must then be reported unavailable or stale. Installing a monitoring agent is an administrator task, not permission for the AI model to obtain a managed-device route or credentials.

The active v3.0 prompt text and byte-preserved v2 archive are not rewritten by this scoped update. Where they mention the small lab fallback, apply this newer explicit deployment profile. Other non-conflicting requirements remain mandatory. The user requested documentation publication, not server installation. Record any future profile change explicitly.

## فارسی

[راهنمای Zabbix](../fa/ZABBIX_SERVER.md) و [رکورد تخصیص](ZABBIX_SERVER_PLAN.json) همراه [پرامپت فعال](NEXTOPS_MASTER_PROMPT.md) خوانده شوند. این اصلاحیه فقط بخش‌های ۱۸ و ۲۲ نسخهٔ ۳.۰، مثال آزمایشگاه اختیاری و مجموع منابع شروع را روشن می‌کند؛ نیازهای امنیت، آفلاین، اتصال‌های اولیه و پذیرش حذف نمی‌شوند.

برای ساخت سرور محلی جدید، `zabbix-server` با **۴ vCPU، حافظهٔ ۱۶ GiB و دیسک ۲۰۰ GiB** و PostgreSQL مستقل، رابط و API زبیکس و Agent 2 در نظر گرفته شود. این ماشین جایگزین پیشنهاد آزمایشگاهیِ ۴ vCPU و ۸ GiB و ۱۰۰ GiB است؛ هر دو به‌طور پیش‌فرض ساخته نشوند. Zabbix موجودِ مناسب و مجاز ابتدا بررسی و استفاده شود، نه بازنویسی.

سه ماشین اولیهٔ NextOps همچنان مجموعاً ۳۶ vCPU، حافظهٔ ۱۶۸ GiB و دیسک ۷۸۰ GiB دارند. با سرور Zabbix، چیدمان فعلی **۴ ماشین، ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB** است. سهم موقت swap در ESXi برابر ۱۸۴ GiB و جمع پیش از سایر سربارها **۱۱۶۴ GiB** می‌شود. تعداد ماشین‌های خود NextOps به‌ترتیب ۳، سپس ۴ با پایگاه جدا و ۵ با اصلاح است؛ با زبیکس مجموع به ۴، ۵ و ۶ می‌رسد. اعداد صرفاً NextOps در راهنمای قدیمی دوباره به این جمع اضافه نشوند.

Zabbix مجاز باید پیش از خواندن زندهٔ 1C آماده باشد و می‌تواند هم‌زمان با 1A و 1B ساخته شود؛ اما توکن مقصد فقط پس از قبولی پایهٔ هویت، سیاست و ممیزی به اتصال‌دهنده برسد. برای پاسخ اول، SSH مستقیم Linux، RAG پیشرفته، پایگاه اضافی یا اصلاح خودکار لازم نیست.

LVM و سیاست پیشنهادی نگهداری در راهنما آمده‌اند. سقف سه‌ترابایتی، نام مستعار DS-C، شروع و پاسخ تازهٔ آفلاین، پشتیبان مستقل و کنترل دقیق عملیات حفظ شوند. در قطع Zabbix، پرسش عمومی محلی با سالم بودن وابستگی‌های خودش باقی بماند؛ شاهد جاری پایش در این حالت غایب یا قدیمی گزارش شود. نصب عامل پایش کار مسئول زیرساخت است، نه مجوز شبکهٔ تجهیزات یا اطلاعات ورود برای مدل.

متن فعال نسخهٔ ۳.۰ و بایگانی دقیق نسخهٔ ۲ در این تغییر محدود بازنویسی نمی‌شوند. در بخش مربوط به آزمایشگاه کوچک، این چیدمان تازه مقدم است؛ سایر نیازهای بدون تعارض پابرجا هستند. درخواست مالک، انتشار مستندات است نه نصب سرور. تغییر بعدی چیدمان نیز صریح ثبت شود.
