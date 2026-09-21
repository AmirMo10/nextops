<div dir="rtl">

# پروندهٔ وابستگی استقرار برای هر سرور

[English](../en/DEPLOYMENT_DOSSIERS.md) · [فهرست](INDEX.md) · [برنامهٔ سرورها](SERVER_PLAN.md) · [شرط ذخیره‌سازی](../STORAGE_PLAN.md)

برای نخستین اقدام‌ها، ترتیب ساخت، فرمان‌های فقط‌خواندنی مهمان و توقف‌های نصب، پیش از باز
کردن تغییر از [چک‌لیست شروع سرورها](SERVER_START_CHECKLIST.md) استفاده کنید.

**وضعیت: قرارداد تحویل همراه installer محافظت‌شدهٔ OS-package؛ نه installer کامل محصول و نه مجوز استقرار.** چهار فایل YAML خوانا در مسیر [`deploy/server-dependencies`](../../deploy/server-dependencies) اندازه‌های معلوم، مرزهای پیشنهادی، وابستگی‌ها، مسیر تنظیمات، الگوهای فرمان، شاهدهای لازم و ورودی‌های حل‌نشدهٔ چیدمان پذیرفته‌شده را یک‌جا ثبت می‌کنند. scriptهای متناظر در [`deploy/installers`](../../deploy/installers) فقط لایهٔ package آفلاین و احرازشده را پوشش می‌دهند. همهٔ دروازه‌های پذیرش اجرایی همچنان `not_run` هستند.

## فایل‌ها و مسئولیت‌ها

| پروندهٔ سرور | مسئولیت | منابع پیشنهادی |
|---|---|---:|
| [`nextops-app.yaml`](../../deploy/server-dependencies/nextops-app.yaml) | TLS، رابط، API، هویت، worker و audit ماندگار و PostgreSQL محدود اولیهٔ NextOps | ۸ vCPU / حافظهٔ ۳۲ GiB / دیسک ۲۰۰ GiB |
| [`nextops-ai.yaml`](../../deploy/server-dependencies/nextops-ai.yaml) | یک سرویس AI محلی روی CPU با فایل‌های مدل و runtime تأییدشده | ۲۴ vCPU / حافظهٔ ۱۲۸ GiB / دیسک ۵۰۰ GiB |
| [`nextops-connectors-ro.yaml`](../../deploy/server-dependencies/nextops-connectors-ro.yaml) | درگاه حفاظت‌شده و runner جدا و فقط‌خواندنی Zabbix | ۴ vCPU / حافظهٔ ۸ GiB / دیسک ۸۰ GiB |
| [`zabbix-server.yaml`](../../deploy/server-dependencies/zabbix-server.yaml) | طرح Zabbix 7.0 LTS مستقل، PostgreSQL 16، رابط/API، Agent 2 و LVM کامل | ۴ vCPU / حافظهٔ ۱۶ GiB / دیسک ۲۰۰ GiB |
| [`server-dependency.schema.json`](../../deploy/server-dependencies/server-dependency.schema.json) | قرارداد عمومی نسخهٔ ۱.۰.۰ برای همهٔ پرونده‌ها | سرور نیست |

[راهنمای مجری installer](../../deploy/installers/README.md) نقش هر سرور را به script ورودی آن نگاشت می‌کند و ساختار bundle، فرمان‌های check/apply، دروازه‌های مجوز و مرز package-only را توضیح می‌دهد.

مجموع پیشنهادی چهار ماشین، ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک مجازی ۹۸۰ GiB است. سهم موقت swap در ESXi نیز ۱۸۴ GiB است و جمع پیش از VMX، snapshot، رشد thin، staging، نگهداری و restore به ۱۱۶۴ GiB می‌رسد. این اعداد ورودی برنامه‌ریزی‌اند؛ نه رزرو و نه اثبات ظرفیت آزاد.

## نخستین کار مسئول استقرار

یک **رکورد خصوصی استقرار بیرون از این مخزن عمومی** بسازید. فقط شناسه‌های بخش `required_inputs` هر پرونده را بردارید و مقدار آنها را با شاهد خصوصی و تأییدشده تکمیل کنید. ترتیب آغاز:

1. `authorization.*` — مقصد دقیق، مجری، عملیات، بازهٔ تغییر و اختیار بازگشت؛
2. `vm.*` — ظرفیت و رقابت جاری ESXi، سازگاری VM، سلامت و فضای datastore، محل swap و جلوگیری از دوباره‌شماری ماشین موجود؛
3. `artifact.*` — release، بسته، مدل، نسخه، امضا یا checksum، مجوز و مسیر بستهٔ آفلاین؛
4. `network.*` و `target.*` — نام و نشانی خصوصی، مسیر، port، اعتماد گواهی، allowlist، نسخه و base path زبیکس و دامنهٔ host group؛
5. `secrets.*` — فقط ارجاع محرمانه، هویت مصرف‌کننده، تحویل، چرخش، لغو، پالایش و بازیابی؛
6. `storage.*` و `recovery.*` — اثبات device و mount، رشد و نگهداری، پشتیبان مستقل، مقصد restore، RPO/RTO و آخرین فایل سالم؛
7. `acceptance.*` — آزمون‌های مصوب کیفیت، زمان پاسخ، بار، خطا، آفلاین و بازیابی.

مقدار `null` را با حدس مناسب‌نما پر نکنید. رکورد خصوصی تکمیل‌شده، hostname و IP واقعی، شناسهٔ واقعی datastore، token، password، کلید خصوصی گواهی یا مقصد پشتیبان را commit نکنید.

## معنای فرمان‌ها

هر فرمان یک `mode` دارد:

| حالت | معنا |
|---|---|
| `read_only` | فرمانی که قرار نیست وضعیت را تغییر دهد؛ اجرای آن روی زیرساخت همچنان مجوز مقصد می‌خواهد و خروجی حساس باید خصوصی بماند. |
| `guarded_template` | الگوی بازبینی‌شده با ورودی‌های نام‌دار. ممکن است script مخزن را فراخوانی کند، اما مجوز عمومی نیست؛ همهٔ ورودی‌ها ابتدا در رکورد خصوصی حل و اعتبارسنجی شوند. |
| `blocked` | هنوز فرمان دقیق و امن در مخزن وجود ندارد. مقدار `command` عمداً `null` است و مانع و شرط لازم کنار آن آمده است. |

سامانه‌ای نسازید که رشته‌های داخل YAML را خودکار و بدون بازبینی اجرا کند. این فایل‌ها قرارداد تحویل برای change procedure بازبینی‌شده‌اند. پیش از هر تغییر، مقصد، مجوز، mount، artifact، permission و authorization دوباره بررسی شوند.

## فرمان‌های اعتبارسنجی

ابتدا وابستگی‌های قفل‌شدهٔ توسعه را نصب و سپس اعتبارسنج مخزن را اجرا کنید:

```bash
uv sync --extra dev --frozen
uv run --extra dev python scripts/check_deployment_dossiers.py
uv run --extra dev python scripts/check_server_installers.py
```

اعتبارسنج هر چهار سند YAML را ایمن parse می‌کند، آنها را با JSON Schema نسخهٔ Draft 2020-12 می‌سنجد، باقی‌ماندن نسخهٔ قدیمی JSON را رد می‌کند، شناسهٔ سرورهای پذیرفته‌شده را کنترل می‌کند و مجموع ۴۰ vCPU، حافظهٔ ۱۸۴ GiB و دیسک ۹۸۰ GiB را تطبیق می‌دهد.

بررسی مستندات مخزن:

```bash
python scripts/check_docs.py
```

قبولی YAML یا schema فقط شکل داده را ثابت می‌کند؛ مقدار خصوصی، اصالت artifact، ظرفیت زیرساخت، رفتار سرویس یا مجوز را تأیید نمی‌کند.

## گردش امن استقرار

1. **واقعیت را تطبیق دهید.** روشن کنید هر VM یا یک Zabbix مناسب از قبل وجود دارد یا نه. چیزی را دوباره نسازید یا دوباره از ظرفیت کم نکنید. شاهد host و DS-C در بازهٔ مجاز تازه شود.
2. **ورودی‌های لازم را ببندید.** تا وقتی ورودی لازم برای گام بعد `missing` یا `pending_authorization` یا `not_run` است، آن سرور جلو نمی‌رود.
3. **artifact را قفل کنید.** نسخهٔ تغییرناپذیر، checksum یا امضا، مجوز، وابستگی گذرا، build flag و یک مجموعهٔ سازگار برای rollback ثبت شود. بستهٔ آفلاین کامل و بدون credential عملیاتی آماده شود.
4. **runbook دقیق را بنویسید و بیازمایید.** فقط چیدمان منتخب و ورودی خصوصی را به فرمان‌های محیط واقعی برای نصب، start، stop، backup و restore تبدیل کنید. ابتدا در آزمایشگاه جدا یا مقصد restore پاک ثابت شوند.
5. **preflight فقط‌خواندنی اجرا کنید.** OS، kernel، CPU و حافظه، mount، فضای آزاد، زمان، listener، گواهی و تعارض سرویس ثبت شود. در تفاوت توقف کنید؛ تفاوت را پنهان نکنید.
6. **هر بار یک سرور را پیش ببرید.** ترتیب `nextops-app` سپس `nextops-ai` سپس `nextops-connectors-ro` حفظ شود و Zabbix پیش از 1C کامل آماده باشد. آمادگی سرویس مبنا باشد، نه sleep ثابت.
7. **مرزها را ثابت کنید.** فقط app به کاربر سرویس می‌دهد؛ inference، پایگاه و gateway داخلی‌اند؛ فقط runner جدا token زبیکس دارد؛ PostgreSQL زبیکس محلی است؛ اینترنت زمان اجرا و همهٔ تغییرات Phase 1 رد می‌شوند.
8. **شاهد پذیرش را ثبت کنید.** خروجی پالایش‌شده، شناسهٔ release، زمان، دامنه، نتیجهٔ آزمون، شکست و skip، سنجهٔ منابع و ارجاع backup/restore در رکورد خصوصی ذخیره شود. دروازهٔ `not_run` فقط با شاهد واقعی در سامانهٔ شاهد تغییر کند.
9. **ارتقا یا بازگشت.** promotion به قبولی دروازه‌های همین پرونده و موارد ZBX/OFF لازم وابسته است. در trigger ثبت‌شده rollback کنید و نتیجهٔ نامعلوم را بررسی کنید، نه اینکه کورکورانه تکرار شود.

## شرط توقف هر سرور

### `nextops-app`

پیش از نصب برنامه توقف کنید. اکنون API در سطح source، migration و role گروهی PostgreSQL، رفتار worker با fixture و scriptهای محافظت‌شده برای لایهٔ package آفلاین و معتبر وجود دارد؛ اما bundle تأییدشدهٔ package، installer/release کامل تولید، UI مرورگر، تحویل login role تولید، reverse proxy، Compose، systemd unit و backup/restore آزموده وجود ندارد. موفقیت نصب package را استقرار محصول ندانید، فرمان CI را runbook تولید نکنید و برای جبران environment variable ساختگی یا PostgreSQL شبکه‌ای نسازید.

### `nextops-ai`

تا commit و build flag دقیق llama.cpp، ISA مهمان، revision و quantization و template و license و checksum مدل، resource profile، احرازهویت داخلی و هدف ارزیابی فارسی/انگلیسی قفل نشده، import یا start انجام نشود. ۲۴ vCPU و ۱۲۸ GiB بودجهٔ آزمایش است، نه thread count یا تضمین کارایی.

### `nextops-connectors-ro`

تا gateway و runner، نسخهٔ پروتکل MCP، endpoint و نسخه و base path زبیکس، گواهی، permission گروه میزبان، allowlist روش و فیلد، سقف‌ها و تحویل token فقط به runner آزموده نشده، به مقصد وصل نشوید. مدل، app، gateway، مرورگر و log نباید مقدار token را بگیرند.

### `zabbix-server`

ابتدا وجود Zabbix مناسب و مجاز بررسی شود. برای VM تازه، تا دیسک مهمانِ خالی و جدید ۲۰۰ GiB با قطعیت شناخته نشده و مجوز مخرب همان دیسک را نام نبرده، storage تغییر نکند. تا `/var/lib/postgresql` واقعاً mount مربوط به LV ۱۱۲ GiB نیست، پایگاه ساخته نشود. قفل بسته، روش امن credential پایگاه، بار پایش، retention، backup و restore نیز الزامی‌اند.

## شاهد لازم برای تحویل

مسئول استقرار برای هر سرور یک رکورد خصوصی با این موارد تحویل می‌دهد:

- نسخهٔ schema و پرونده و commit گیت؛
- شناسهٔ change و authorization، مجری، مقصد، زمان آغاز و پایان و عملیات دقیق؛
- شناسهٔ ورودی‌های حل‌شده با ارجاع شاهد و طبقه‌بندی؛
- مقدار واقعی VM، OS، منابع، storage و network و تفاوت با پیشنهاد؛
- نسخه، checksum یا امضا، license و موجودی بستهٔ آفلاین؛
- هویت و permission سرویس‌های ساخته‌شده و مصرف‌کنندهٔ secret reference، بدون مقدار محرمانه؛
- فرمان دقیق یا نسخهٔ runbook و نتیجهٔ خروج؛
- نتیجهٔ readiness، مرز امنیت، آفلاین، بار، خطا، backup، restore و rollback؛
- مانع باقی‌مانده، مورد skipped یا not-run و گام مجاز بعدی.

مخزن، قرارداد عمومی می‌ماند. رکورد خصوصی استقرار، منبع اصلی مقدارهای محیط و شاهد عملیاتی است.

</div>
