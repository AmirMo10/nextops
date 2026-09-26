<div dir="rtl">

# راهنمای رفع موانع پذیرش تولید

[English](../en/PRODUCTION_BLOCKERS_RUNBOOK.md) · [قرارداد بازیابی](../../deploy/recovery/README.md) · [وضعیت جاری](../status/current-release.yaml)

**وضعیت: اقدام مالک لازم است؛ این سند به‌تنهایی هیچ دروازه‌ای را نمی‌بندد.** به‌روزرسانی: ۴ مهر ۱۴۰۵، برابر با ۲۶ سپتامبر ۲۰۲۶.

ترتیب کنونی تحویل تغییر کرده است: مالک می‌گوید از هر چهار سرور هر روز در ESXi ‏snapshot گرفته
می‌شود و کار بازیابی مستقل را برای این استقرار محلی به تعویق انداخته است. بخش‌های ۳ و ۴ برای
تحویلِ احتمالی آینده حفظ شده‌اند، نه به‌عنوان نخستین کار فعال. برنامهٔ snapshot و نتیجهٔ بازیابی
آن مستقلاً بررسی نشده‌اند و پشتیبان مستقل را اثبات نمی‌کنند. پروفایل بازیابی مسدود می‌ماند و پذیرش کامل تولید هنوز
ممکن نیست. طبق [کار بعدی](../NEXT_TASK.md)، ابتدا کیفیت معنایی پاسخ دوزبانهٔ انتشار جاری و سپس
دروازه‌های غیربازیابیِ انتشار، امنیت و بهره‌برداری پیگیری شوند. این تعویق، مجوز تغییر سرورها نیست.

مالک سپس روشن کرد که بازیابی از snapshot ماشین ESXi را شخصاً آزموده است؛ گزارش تاریخ‌دار این
آزمون در این بازبینی بررسی نشده و معیارهای بازیابی مستقل را کامل نمی‌کند.

مالک در ۴ مهر ۱۴۰۵ تأیید کرد که منابع مستقل پشتیبان و آزمایش بازیابی، تصمیم مجوز پروژه، مسیر
داخلی تحویل اعلان و گیرندگان، جفت گواهی جایگزین CA و تأییدکنندگان نام‌دار هنوز در دسترس نیستند.
گام‌های زیر دستور تحویل در آینده‌اند؛ مقدار موقت یا کپی روی مهمان سرویس‌دهنده جایگزین آن‌ها نیست.

این راهنما همهٔ موانعی را که هنوز اجازهٔ ادعای «پذیرش تولید» نمی‌دهند فهرست می‌کند و کارهای مالک را
از کارهایی که عامل مهندسی NextOps پس از تحویل ورودی‌ها انجام می‌دهد جدا نگه می‌دارد. نشانی، شناسهٔ
datastore، گذرواژه، توکن، کلید خصوصی، راز SMTP، کلید CA یا موجودی خام زیرساخت نباید در Git، issue
یا گفتگو قرار گیرد. این مقدارها فقط در پروندهٔ خصوصی تغییر نگه‌داری شوند.

فرمان‌های این سند یا فقط‌خواندنی‌اند یا حساب و فایل تازه می‌سازند. تا وقتی مقصد دقیق مشخص و
بازبینی نشده، هیچ فرمان قالب‌بندی دیسک، حذف پایگاه، ترویج گواهی یا تغییر دیوارهٔ آتش ارائه نشده
است. اگر خروجی مورد انتظار غایب یا متفاوت بود، توقف کنید و مسیر یا device را حدس نزنید.

## ۱. موانع جاری و مسئول هرکدام

| شناسه | وضعیت فعلی | اقدام مالک | اقدام مهندسی پس از تحویل مالک | شرط خروج |
|---|---|---|---|---|
| `independent_destination_not_approved` | مسدود؛ به‌تعویق‌افتاده به دستور مالک | ذخیره‌سازی بیرون از همهٔ VMهای سرویس‌دهنده، datastore و hypervisor آن‌ها ایجاد و تصویب شود | مخزن‌های جداگانهٔ pgBackRest و restic صلاحیت‌سنجی و پیکربندی شوند | شاهد استقلال پذیرفته شود |
| `recovery_objectives_not_approved` | مسدود؛ به‌تعویق‌افتاده به دستور مالک | RPO، RTO، نگه‌داری، تناوب restore، مالک‌ها و حضانت کلید تصویب شود | مقدارهای پالایش‌شده در پروفایل بازیابی ثبت شوند | سیاست امضا و پروفایل معتبر شود |
| `offline_tool_bundles_not_verified` | مسدود؛ به‌تعویق‌افتاده به دستور مالک | محیط build/staging متصل و سیاست مجوزها تصویب شود | pgBackRest 2.59.1 و restic 0.19.1 دریافت، هش، بازبینی مجوز و آفلاین آزموده شوند | نصب/حذف آفلاین نسخه‌های دقیق و ثبت hash موفق باشد |
| `isolated_restore_not_run` | مسدود؛ به‌تعویق‌افتاده به دستور مالک | محیط restore جدا، بدون مسیر و اطلاعات ورود تولید فراهم شود | آزمون کامل/تفاضلی/WAL/PITR، فایل، منفی، آفلاین و بازیابی کلید اجرا شود | همهٔ دروازه‌ها با RPO/RTO اندازه‌گیری‌شده موفق شوند |
| تحویل اعلان گواهی به بهره‌بردار | ناقص | مسیر اعلان محلی LAN و گیرندهٔ اصلی/پشتیبان نام‌گذاری شود | media، user media، action و پیام بازیابی Zabbix پیکربندی شود | پیام مشکل و بازیابی کنترل‌شده به هر دو گیرنده برسد |
| چرخش و بازگشت گواهی | اجرا نشده | دو جفت جایگزین امضاشده با CA و پنجرهٔ تغییر فراهم شود | هر رابط با guard آماده، بررسی، چرخانده، آزموده و برگردانده شود | چرخش و بازگشت هر دو با اعتبارسنجی عادی TLS موفق باشد |
| وابستگی، مجوز، SBOM و یکپارچگی انتشار | باز | مسئول حقوقی/امنیتی و سیاست پذیرش تعیین شود | SBOM، موجودی مجوز، شاهد آسیب‌پذیری و مادهٔ راستی‌آزمایی آفلاین ساخته و بازبینی شود | وابستگی یا مجوز ردشده و یافتهٔ حل‌نشده باقی نماند |
| سیاست شبکهٔ میزبان | ناقص | بازه‌های مبدأ مجاز SSH مدیریتی و مسیرهای خروجی DNS، زمان و پراکسی نگه‌داری تصویب شوند | فهرست مجاز کل میزبان همراه امکان بازگشت اعمال و آزمون تازهٔ آفلاین و نگه‌داری تکرار شود؛ مرز پذیرفته‌شدهٔ اتصال‌دهنده حفظ گردد | شبکهٔ داخلی و پراکسی مجاز کار کنند و خروجی عمومی مستقیم و مبدأ SSH غیرمجاز رد شوند |
| تصمیم نهایی تولید | اجرا نشده | مسئول تصویب تولید، پروفایل محدود و پذیرفته‌شده را امضا کند | همهٔ دروازه‌های تولید تکرار و فقط نتیجهٔ پالایش‌شده منتشر شود | هیچ دروازهٔ الزامی شکست‌خورده، ناقص یا اجرا‌نشده نباشد |

چهار شناسهٔ نخست، دقیقاً همان موانع ماشین‌خوان فایل `deploy/recovery/recovery-profile.yaml` هستند.
پنج مورد دیگر دروازه‌های صریح وضعیت جاری پروژه‌اند.

## ۲. ساخت پروندهٔ خصوصی تصمیم‌های مالک

این فرمان‌ها را روی رایانهٔ توسعهٔ Windows اجرا کنید. مسیر ساخته‌شده بیرون مخزن است.

```powershell
$QualificationDir = Join-Path $HOME '.nextops\production-qualification'
New-Item -ItemType Directory -Force -Path $QualificationDir | Out-Null
$DecisionFile = Join-Path $QualificationDir 'owner-decisions.txt'
New-Item -ItemType File -Force -Path $DecisionFile | Out-Null
notepad $DecisionFile
```

قالب زیر را در فایل قرار دهید و همهٔ مقدارهای `REQUIRED` را تکمیل کنید. سیاست پیشنهادی نقطهٔ شروع
است و تأیید کسب‌وکار از روی سکوت استنباط نمی‌شود.

```text
change_id=REQUIRED
owner_approver=REQUIRED
recovery_operator=REQUIRED
rollback_owner=REQUIRED
maintenance_window=REQUIRED
management_ssh_source_ranges=REQUIRED_PRIVATE_RECORD
host_dns_time_proxy_egress_routes=REQUIRED_PRIVATE_RECORD

destination_id=REQUIRED_NON_SECRET_ALIAS
destination_type=dedicated_physical_or_separate_hypervisor
independent_from_serving_guest=yes
independent_from_serving_datastore=yes
independent_from_serving_hypervisor=yes

rpo_minutes=15
rto_minutes=240
full_backups_to_keep=4
differential_backups_to_keep=14
wal_days_to_keep=14
file_snapshots_to_keep=30
restore_test_cadence=quarterly

key_custodian_primary=REQUIRED
key_custodian_secondary=REQUIRED_DIFFERENT_PERSON
offline_recovery_copy_location=REQUIRED_PRIVATE_REFERENCE

notification_type=internal_smtp_or_approved_lan_route
notification_owner_primary=REQUIRED
notification_owner_backup=REQUIRED
notification_recipient_primary=REQUIRED_PRIVATE_REFERENCE
notification_recipient_backup=REQUIRED_PRIVATE_REFERENCE

certificate_issuer=REQUIRED_PRIVATE_REFERENCE
certificate_change_window=REQUIRED
certificate_rollback_owner=REQUIRED

license_approver=REQUIRED
security_approver=REQUIRED
production_approver=REQUIRED
```

این فایل را در گفتگو paste نکنید. فقط تصمیم‌های غیرمحرمانه را ارسال کنید و اعلام کنید که پروندهٔ
خصوصی کامل شده است.

## ۳. ایجاد مقصد مستقل بازیابی

### ۳.۱ طراحی الزامی

پیشنهاد اصلی، یک میزبان فیزیکی مستقل با Ubuntu Server 24.04 LTS و ذخیره‌سازی محافظت‌شده است. گزینهٔ
دیگر، VM روی hypervisor فیزیکی و ذخیره‌سازی پشتیِ متفاوت است. VM پنجم روی hypervisor فعلی، دیسک
مجازی دیگر روی datastore فعلی، NFS متکی به همان میزبان، snapshot یا پوشه‌ای روی یکی از VMهای
سرویس‌دهنده این دروازه را برآورده نمی‌کند.

مقصد بازیابی باید هنگام قطع اینترنت عمومی از شبکهٔ مدیریتی مصوب در دسترس بماند و اطلاعات ورود را
به مدل یا برنامه ندهد. برای پایگاه برنامه، پایگاه Zabbix و فایل‌های مجاز restic، مخزن و هویت دسترسی
جدا لازم است.

یک VM موقت restore یا محیط فیزیکی جدا نیز آماده کنید. این محیط نباید مسیر شبکه یا اعتبارنامهٔ
اتصال‌دهنده، API زبیکس یا برنامهٔ تولید را داشته باشد. اندازه‌گذاری باید از اندازهٔ واقعی داده و
حداقل ۳۰ درصد فضای کاری اضافه انجام شود؛ مصرف فعلی thin مبنای حدس نیست.

### ۳.۲ اندازه‌گیری ظرفیت محافظت‌شده

فرمان‌ها را روی رایانهٔ توسعه اجرا و خروجی را فقط در پروندهٔ خصوصی نگه دارید.

```powershell
$QualificationDir = Join-Path $HOME '.nextops\production-qualification'
$MeasureFile = Join-Path $QualificationDir 'source-capacity.txt'
@(
  '=== application PostgreSQL bytes ==='
  (ssh nextops-app 'sudo -n -u postgres psql --cluster 16/nextops -d postgres -Atc "SELECT COALESCE(sum(pg_database_size(datname)),0) FROM pg_database WHERE datistemplate = false;"')
  '=== Zabbix PostgreSQL bytes ==='
  (ssh nextops-zabbix 'sudo -n -u postgres psql --cluster 16/zabbix -d postgres -Atc "SELECT COALESCE(sum(pg_database_size(datname)),0) FROM pg_database WHERE datistemplate = false;"')
  '=== approved artifact candidate bytes ==='
  (ssh nextops-app "sudo -n du -sb /srv/nextops/releases /usr/local/share/doc/nextops 2>/dev/null")
  (ssh nextops-ai "sudo -n du -sb /srv/nextops/releases /srv/nextops/models 2>/dev/null")
  (ssh nextops-connectors "sudo -n du -sb /srv/nextops/releases 2>/dev/null")
) | Set-Content -Encoding utf8 $MeasureFile
Get-Content $MeasureFile
```

اندازهٔ پایگاه، نرخ تغییر روزانه، نگه‌داری منتخب و فضای کاری restore مبنای ظرفیت‌اند. عامل مهندسی
پس از مشاهدهٔ نرخ WAL/تغییر، ذخیرهٔ نهایی مخزن را محاسبه می‌کند.

### ۳.۳ ساخت دسترسی مدیریتی کنترل‌شده

روی Windows یک کلید اختصاصی برای میزبان بازیابی بسازید. کلید اتصال‌دهنده، برنامه یا مدیریت عادی
دوباره استفاده نشود. `ssh-keygen` گذرعبارت می‌خواهد؛ گذرعبارت محافظت‌شده تعیین و کلید در SSH agent
ویندوز بار شود.

```powershell
$RecoveryKey = Join-Path $HOME '.ssh\nextops_recovery_ed25519'
if (Test-Path -LiteralPath $RecoveryKey) { throw 'Recovery key already exists; inspect it instead of overwriting it.' }
ssh-keygen -t ed25519 -a 64 -f $RecoveryKey -C 'nextops-recovery-deployment'
Get-Service ssh-agent | Set-Service -StartupType Automatic
Start-Service ssh-agent
ssh-add $RecoveryKey
Get-Content "$RecoveryKey.pub"
```

در console محلی یا مجازیِ مورد اعتماد میزبان تازه اجرا کنید:

```bash
id nextops-dev >/dev/null 2>&1 || sudo adduser --disabled-password --gecos '' nextops-dev
sudo passwd -l nextops-dev
sudo install -d -o nextops-dev -g nextops-dev -m 0700 /home/nextops-dev/.ssh
sudoedit /home/nextops-dev/.ssh/authorized_keys
sudo chown nextops-dev:nextops-dev /home/nextops-dev/.ssh/authorized_keys
sudo chmod 0600 /home/nextops-dev/.ssh/authorized_keys
printf '%s\n' 'nextops-dev ALL=(ALL:ALL) NOPASSWD: ALL' \
  | sudo tee /etc/sudoers.d/90-nextops-dev >/dev/null
sudo chmod 0440 /etc/sudoers.d/90-nextops-dev
sudo visudo -cf /etc/sudoers.d/90-nextops-dev
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

فقط یک خط کلید عمومی در `authorized_keys` قرار دهید. فرمان آخر fingerprint میزبان را می‌نویسد؛
فقط همان fingerprint از مسیر مستقل و تأییدشده ارسال شود.

روی Windows، کلید شبکه را بگیرید اما تا تطبیق دقیق fingerprint آن را معتبر ندانید:

```powershell
$RecoveryHost = Read-Host 'Recovery host IP or FQDN'
$Candidate = Join-Path $env:TEMP 'nextops-recovery-hostkey'
ssh-keyscan -t ed25519 $RecoveryHost 2>$null | Set-Content -Encoding ascii $Candidate
ssh-keygen -lf $Candidate
```

پس از تطبیق دستی و دقیق با fingerprint کنسول:

```powershell
Get-Content $Candidate | Add-Content -Encoding ascii "$HOME\.ssh\nextops_known_hosts"
Remove-Item -LiteralPath $Candidate
notepad "$HOME\.ssh\config"
```

بلوک زیر را با جایگزینی فقط نام یا نشانی خصوصی اضافه کنید:

```sshconfig
Host nextops-recovery
    HostName RECOVERY_HOST_OR_IP
    User nextops-dev
    IdentityFile ~/.ssh/nextops_recovery_ed25519
    UserKnownHostsFile ~/.ssh/nextops_known_hosts
    IdentitiesOnly yes
    StrictHostKeyChecking yes
    BatchMode yes
    ConnectTimeout 10
    ServerAliveInterval 30
    ServerAliveCountMax 3
    ForwardAgent no
```

حساب را بدون تغییر میزبان بررسی کنید:

```powershell
ssh -o BatchMode=yes nextops-recovery "id; sudo -n true; systemd-detect-virt; systemctl is-system-running"
```

دسترسی کامل و بدون گذرواژهٔ sudo فقط برای استقرار کنترل‌شده و موقت است. پس از صلاحیت‌سنجی، آن را
با قواعد فرمان‌محور بازبینی‌شده جایگزین یا حذف کنید:

```bash
sudo rm -f /etc/sudoers.d/90-nextops-dev
sudo visudo -c
```

پیش از وجود و آزمون مسیر مدیریت اضطراری، این دسترسی حذف نشود.

### ۳.۴ ثبت شاهد استقلال و سلامت

روی میزبان بازیابی اجرا و خروجی کامل را فقط در پروندهٔ خصوصی نگه دارید:

```bash
cat /etc/os-release
uname -r
systemd-detect-virt
sudo dmidecode -s system-manufacturer
sudo dmidecode -s system-product-name
sudo dmidecode -s system-uuid
lsblk -e7 -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS,MODEL,SERIAL
findmnt -T /srv/nextops-recovery -o SOURCE,TARGET,FSTYPE,OPTIONS
df -B1 /srv/nextops-recovery
timedatectl status
ip -brief address
ip route
ss -H -lntup
systemctl --failed --no-legend
```

مالک باید شناسهٔ hypervisor/دارایی فیزیکی و شناسهٔ ذخیره‌سازی پشتی را نیز از صفحهٔ مدیریت ثبت کند؛
فرمان داخل مهمان به‌تنهایی استقلال دامنهٔ خرابی را ثابت نمی‌کند. این شناسه‌ها در Git عمومی یا
گفتگو قرار نگیرند. تا پیش از بازبینی device خالی و مسیر بازگشت، فرمان‌های `mkfs`، `wipefs`،
`fdisk`، `parted`، ساخت LVM، تغییر mount یا دیوارهٔ آتش اجرا نشوند.

### ۳.۵ تصمیم‌های شبکه‌ای لازم

در ابتدا فقط این جریان‌ها تصویب شوند:

- رایانهٔ مدیریت به میزبان بازیابی: SSH روی TCP 22؛
- میزبان PostgreSQL برنامه و میزبان بازیابی: مسیر SSH بازبینی‌شدهٔ pgBackRest؛
- میزبان PostgreSQL زبیکس و میزبان بازیابی: مسیر SSH بازبینی‌شدهٔ pgBackRest؛
- کارخواه‌های فایل مصوب به میزبان بازیابی: مسیر انتقال منتخب restic؛
- میزبان بازیابی و آزمایشگاه restore فقط به DNS، زمان و پایش محلی مصوب.

ورودی اینترنت عمومی، ورودی رابط برنامه، دسترسی مدل، مسیر عمومی اتصال‌دهنده یا مسیر آزمایشگاه restore
به مقصدهای تولید مجاز نیست. مالک دیوارهٔ آتش و شناسهٔ قواعد خصوصی ثبت شود. پس از تصویب مقصد و
transport، مهندسی قواعد دقیق مبدأ و مقصد را ارائه می‌کند.

## ۴. تصویب اهداف بازیابی و حضانت کلید

مقادیر اولیهٔ پیشنهادی عبارت‌اند از RPO برابر ۱۵ دقیقه، RTO برابر ۲۴۰ دقیقه، چهار پشتیبان کامل،
چهارده پشتیبان تفاضلی، چهارده روز WAL، سی snapshot فایل و تمرین restore فصلی. این مقادیر باید با
نرخ تغییر واقعی، ظرفیت مقصد و نیاز کسب‌وکار سنجیده شوند. مالک باید صریحاً `approved` بنویسد یا
مقدار جایگزین بدهد؛ سکوت تأیید نیست.

دو شخص متفاوت باید بتوانند مادهٔ رمزنگاری مخزن را بازیابی کنند. رمز یا نسخهٔ بازیابی آن نباید در
Git، خود مخزن پشتیبان، همان حساب password manager اعتبارنامهٔ مخزن یا گفتگو نگه‌داری شود. فقط
مرجع خصوصی و تاریخ آزمون موفق بازیابی کلید ثبت شود.

پس از تکمیل پرونده، فقط خلاصهٔ غیرمحرمانهٔ زیر را ارسال کنید:

```text
destination_alias=<non-secret alias>
independence=guest:yes,datastore:yes,hypervisor:yes
rpo_minutes=<approved integer>
rto_minutes=<approved integer>
retention=full:<n>,diff:<n>,wal_days:<n>,files:<n>
restore_cadence=<approved cadence>
key_custody=two-person-approved
recovery_host_access=ready
restore_lab=ready
```

## ۵. دروازهٔ بستهٔ آفلاین ابزارهای پشتیبان

پس از تکمیل بخش‌های ۲ تا ۴، مهندسی بسته‌های دقیق pgBackRest 2.59.1 و restic 0.19.1 را در محیط
build موقت و متصل آماده می‌کند. مالک باید مجوزهای MIT و BSD-2-Clause و استفاده از آن محیط staging
را تصویب کند. روی VM سرویس‌دهنده `apt install`، `curl | sh` یا compile اجرا نشود و VM سرویس‌دهنده
نباید بسته دانلود کند.

مهندسی باید این موارد را تحویل و راستی‌آزمایی کند:

- موجودی دقیق artifact و dependency همراه SHA-256؛
- رکورد مجوز؛
- نسخهٔ کاملاً برابر pgBackRest در میزبان مخزن و پایگاه؛
- نصب، نمایش نسخه، حذف و نصب دوبارهٔ آفلاین؛
- جلوگیری از شروع سرویس یا تغییر پایگاه هنگام staging؛
- نسخهٔ تغییرناپذیر و محفوظ از بسته‌های پذیرفته‌شده.

راهنمای رسمی pgBackRest بر برابری نسخهٔ محلی و راه دور تأکید دارد. موفقیت نصب بسته یا اجرای backup
به‌تنهایی این دروازه را نمی‌بندد.

## ۶. پذیرش پشتیبان و restore جدا

پس از تصویب مقصد، سیاست و بسته‌ها، مهندسی ـ نه مالک ـ در یک تغییر ثبت‌شده این موارد را نصب و
پیکربندی می‌کند:

۱. هویت و مخزن جداگانهٔ pgBackRest برای `nextops-application-postgresql` و
`nextops-zabbix-postgresql`.

۲. زمان‌بندی کامل و تفاضلی، بایگانی پیوستهٔ WAL، نگه‌داری و بررسی مخزن.

۳. restic فقط برای پیکربندی، مستندات، شواهد مجاز، انتشارها و مانیفست‌های مصوب. پوشهٔ دادهٔ
PostgreSQL، snapshot زندهٔ پایگاه، WAL و راز تأییدنشده همچنان ممنوع‌اند.

۴. restore جداگانهٔ هر دو خوشهٔ PostgreSQL 16 و همهٔ رده‌های فایل مصوب.

۵. PITR با اینترنت قطع.

۶. آزمون قطع job، خرابی، WAL مفقود، کلید اشتباه، نسخهٔ ناسازگار و کمبود فضا.

۷. بازیابی کلید توسط متولی دوم.

۸. بررسی سازگاری برنامه و Zabbix، هویت، مجوز، نشست، ممیزی و منشأ شاهد.

۹. ثبت RPO، RTO، CPU، حافظه، فضای ذخیره‌سازی و پاک‌سازی اندازه‌گیری‌شده.

مالک باید پنجرهٔ تغییر را فراهم کند و برای گام بازیابی کلید و مشاهدهٔ نهایی restore حاضر باشد.
تولید تا موفقیت فرمان زیر مسدود است:

```powershell
$env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe scripts/check_recovery_profile.py --require-qualified
```

## ۷. پیکربندی مسیر اعلان گواهی با مالک مشخص

پیشنهاد سازگار با آفلاین، relay داخلی SMTP در شبکهٔ مدیریت است. mailbox صرفاً ابری، webhook
Slack/Teams یا درگاه SMS اینترنتی نباید تنها مسیر باشد. اگر SMTP داخلی وجود ندارد، media type
محلی دیگری در Zabbix تصویب و مالک، مرز دسترس‌پذیری و مسیر بازیابی آن ثبت شود.

این مقدارها خصوصی ثبت شوند:

- میزبان SMTP، درگاه، شیوهٔ TLS و مسیر اعتماد CA؛
- شیوهٔ احرازهویت و مرجع اعتبارنامهٔ محافظت‌شده، در صورت نیاز؛
- فرستنده و گیرندهٔ اصلی و پشتیبان؛
- برنامهٔ ۲۴×۷ یا زمان فعال مصوب؛
- مسئول acknowledge و escalation.

از میزبان Zabbix، بدون ارسال اعتبارنامه، دسترسی TLS را آزمون کنید. مقدارها تعاملی وارد شوند تا در
history پوسته نمانند:

```bash
read -r -p 'SMTP host: ' SMTP_HOST
read -r -p 'SMTP STARTTLS port: ' SMTP_PORT
timeout 15 openssl s_client -starttls smtp \
  -connect "${SMTP_HOST}:${SMTP_PORT}" -servername "$SMTP_HOST" \
  -verify_return_error </dev/null
unset SMTP_HOST SMTP_PORT
```

سپس در رابط Zabbix:

۱. در `Alerts → Media types`، media type داخلی مصوب را بسازید یا فعال کنید، برای TLS کنترل peer و
host را فعال و گزینهٔ **Test** را اجرا کنید.

۲. در `Users → Users → <operator> → Media`، هر دو گیرنده، بازهٔ زمانی مصوب و دست‌کم severityهای
High/Disaster را اضافه کنید.

۳. در `Alerts → Actions → Trigger actions`، action مستقلی بسازید که فقط tag برابر
`component=nextops-certificate` را بپذیرد و پیام مشکل و بازیابی را فقط از media type مصوب بفرستد.

۴. آزمون محافظت‌شدهٔ قطع و بازیابی timer گواهی تکرار شود. هر دو گیرنده باید هر دو پیام را تأیید
کنند و بخش `Alerts` زبیکس تحویل موفق را نشان دهد.

media type دارای گذرواژهٔ SMTP را export نکنید؛ مستند Zabbix هشدار می‌دهد که export تنظیم email
می‌تواند گذرواژه را به‌صورت متن آشکار دربر داشته باشد.

## ۸. تأمین گواهی‌های جایگزین برای تمرین چرخش و بازگشت

از CA داخلی یا آفلاین سازمان استفاده شود. گواهی self-signed نامعتبر برای تولید ساخته نشود و کلید
خصوصی CA یا leaf از راه گفتگو یا Git جابه‌جا نشود.

روی هر رابط، مسیر گواهی و مجموعهٔ SAN فعلی را به‌صورت خصوصی شناسایی کنید:

```bash
sudo sed -n 's/^NEXTOPS_CERTIFICATE_PATH=//p' /etc/nextops/certificate-check.env
sudo sh -c '. /etc/nextops/certificate-check.env; openssl x509 \
  -in "$NEXTOPS_CERTIFICATE_PATH" -noout -issuer -dates -ext subjectAltName'
```

گواهی leaf تازه باید نام‌های لازم فعلی، الگوریتم کلید مصوب و دورهٔ اعتبار سازگار با هشدار ۹۰روزه
داشته باشد. کلید خصوصی ترجیحاً روی مقصد یا workstation آفلاین و مصوب PKI ساخته شود. مالک یا
بهره‌بردار CA باید برای هر رابط این موارد را تحویل دهد:

- گواهی leaf و زنجیرهٔ میانی لازم؛
- کلید خصوصی متناظر از مسیر محافظت‌شده؛
- زنجیرهٔ CA صادرکننده که از قبل نزد کارخواه‌ها مورد اعتماد است؛
- fingerprint و تاریخ انقضای غیرمحرمانه؛
- مرجع صادرکننده/تغییر و روش ابطال.

پیش از تحویل، روی workstation محافظت‌شدهٔ PKI بررسی کنید:

```bash
CERT_FILE='replacement.crt'
KEY_FILE='replacement.key'
CA_FILE='approved-ca-chain.crt'
openssl x509 -in "$CERT_FILE" -noout -dates -ext subjectAltName
openssl verify -CAfile "$CA_FILE" "$CERT_FILE"
CERT_KEY_SHA="$(openssl x509 -in "$CERT_FILE" -pubkey -noout \
  | openssl pkey -pubin -outform DER 2>/dev/null | sha256sum | awk '{print $1}')"
PRIVATE_KEY_SHA="$(openssl pkey -in "$KEY_FILE" -pubout -outform DER 2>/dev/null \
  | sha256sum | awk '{print $1}')"
test "$CERT_KEY_SHA" = "$PRIVATE_KEY_SHA"
unset CERT_KEY_SHA PRIVATE_KEY_SHA
```

پس از staging محافظت‌شده و تأیید مالک، مهندسی guard بازگشت خودکار را فعال، جفت فعلی را حفظ،
مالکیت و تطبیق جفت/زنجیره/SAN/انقضا را بررسی، Nginx را اعتبارسنجی، ترویج اتمی و reload و سپس TLS
عادی مرورگر/API را با اینترنت قطع آزمون می‌کند. بعد جفت پیشین بازگردانده و همهٔ آزمون‌ها تکرار
می‌شوند. پایان تمرین باید روی جفتی باشد که صریحاً تصویب شده؛ این تمرین مجوز تغییر نام‌ها، ریشهٔ
اعتماد یا سیاست اعتبارسنجی نیست.

## ۹. تصویب وابستگی، مجوز، SBOM و یکپارچگی انتشار

یک مسئول حقوقی/مجوز و یک مسئول امنیت در پروندهٔ خصوصی نام‌گذاری شوند. سیاست‌های پیشنهادی زیر تصویب
یا با مقدار جایگزین ثبت شوند:

```text
sbom_formats=SPDX_JSON_and_CycloneDX_JSON
release_license_rule=no_unknown_or_unapproved_license
vulnerability_database_max_age_days=7
critical_vulnerability_rule=zero_unresolved_without_written_exception
high_vulnerability_rule=zero_unresolved_without_written_exception
signature_verification=offline_required
signing_key_custody=separate_from_release_builder
```

artifactهای اصلی فعلی برای llama.cpp و pgBackRest مجوز MIT، برای مدل Qwen مجوز Apache-2.0 و برای
restic مجوز BSD-2-Clause ثبت کرده‌اند. این فهرست، موجودی کامل مجوزهای transitive نیست. مهندسی SBOM
می‌سازد، همهٔ packageها و مجوزها را تطبیق می‌دهد، artifactها را با تاریخ تازگی پایگاه آسیب‌پذیری
آفلاین می‌سنجد، Gitleaks را حفظ، امضای انتشار با راستی‌آزمایی آفلاین را ارزیابی و استثناها را برای
تأیید صریح ارائه می‌کند. فهرست اصلی نباید به‌اشتباه تأیید همهٔ وابستگی‌ها تلقی شود.

## ۹الف. تصویب مرز شبکهٔ میزبان

واحدهای برنامه، API هوش مصنوعی و مدل سیاست IP فقط-loopback دارند و فرایند اتصال‌دهنده با فهرست
مجازِ آزموده‌شده به شبکهٔ داخلی همان استقرار محدود است. این کنترل‌ها اینترنت عمومی IPv4 را برای
پوستهٔ مدیریتی یا همهٔ فرایندهای میزبان نمی‌بندند؛ آزمون قطع WAN چهار مهمان موقت بود. قاعدهٔ
فعلی OpenSSH در UFW نیز تا تعیین سیاست مبدأ مدیریتی، هر مبدأ دارای مسیر به مهمان را مجاز می‌کند.
بازه‌های مبدأ مجاز SSH، منبع DNS و زمان، پراکسی نگه‌داری، مخزن‌های به‌روزرسانی لازم و راه بازگشت
در پروندهٔ خصوصی مالک ثبت شوند؛ نشانی یا مسیر واقعی در Git قرار نگیرد.

پیش‌بررسی فقط‌خواندنی روی هر مهمان:

```bash
ip -4 route
resolvectl status
sudo ufw status numbered
```

روی اتصال‌دهنده، سیاست مؤثر فرایند با
`sudo systemctl show nextops-connector.service -p IPAddressDeny -p IPAddressAllow` نیز بررسی شود.
پس از تصویب موجودی دقیق شبکه، مهندسی بازگشت زمان‌دار آماده می‌کند، فهرست مجاز سطح میزبان را
به‌ترتیب اعمال می‌کند، ورود تازهٔ SSH فقط‌کلیدی و نگه‌داریِ مجاز شبکهٔ داخلی/پراکسی را می‌آزماید
و سپس مرورگر تازهٔ دوزبانه، شواهد Zabbix/Linux و منع مستقیم IPv4/IPv6 را تکرار می‌کند. از این
راهنما نباید قاعدهٔ سراسریِ حدسی برای دیوارهٔ آتش استخراج و اعمال شود.

## ۱۰. پذیرش نهایی تولید

پس از موفقیت همهٔ دروازه‌های بالا، مسئول تولید باید شاهد پالایش‌شده را بازبینی و تصمیم تاریخ‌دار
شامل شناسهٔ انتشار پذیرفته‌شده، دامنه، RPO/RTO، ریسک باقیمانده، مسئول rollback و تاریخ بازبینی/انقضا
را امضا کند. سپس مهندسی این فرمان‌ها را تکرار می‌کند:

```powershell
$env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe -m ruff format --check packages migrations tests scripts deploy/installers
.\.venv\Scripts\python.exe -m ruff check packages migrations tests scripts deploy/installers
.\.venv\Scripts\python.exe -m mypy packages tests scripts deploy/installers
.\.venv\Scripts\python.exe -m pytest -m "not integration and not browser" -q
.\.venv\Scripts\python.exe -m pytest -m browser -q
.\.venv\Scripts\python.exe scripts/check_docs.py
.\.venv\Scripts\python.exe scripts/check_release_status.py
.\.venv\Scripts\python.exe scripts/check_recovery_profile.py --require-qualified
```

کارهای CI برای PostgreSQL 16 و 17، مرورگر و پویش راز نیز باید برای همان commit نهایی موفق باشند.
ورود تازه و آفلاین، تولید پاسخ، دریافت شاهد، restart سرویس، reboot ترتیبی VMها، بازیابی وابستگی،
backup/restore، اعلان و چرخش/بازگشت گواهی باید برای همان انتشار ثبت شوند. تا وقتی دروازه‌ای
`failed`، `partial` یا `not_run` است، تولید پذیرفته نیست.

## ۱۱. آنچه پس از اقدامات مالک باید ارسال شود

فقط checklist پالایش‌شدهٔ زیر را بفرستید؛ پروندهٔ خصوصی و اطلاعات ورود ارسال نشود:

```text
[ ] Independent recovery host provisioned
[ ] Different hypervisor/storage failure domain privately verified
[ ] Restore lab isolated and ready
[ ] SSH host fingerprint independently verified
[ ] nextops-recovery access tested
[ ] RPO/RTO/retention/cadence approved
[ ] Two-person key custody approved
[ ] Connected offline-bundle staging approved
[ ] Internal notification route and two recipients approved
[ ] Replacement app and Zabbix certificate pairs available through protected handoff
[ ] License approver named
[ ] Security approver named
[ ] Production approver named
change_id=<non-secret identifier>
```

پس از تکمیل این فهرست، مهندسی می‌تواند بدون درخواست گذرواژه یا کلید خصوصی در گفتگو ادامه دهد.

## منابع رسمی

- [راهنمای pgBackRest 2.59.1](https://pgbackrest.org/user-guide.html)
- [بررسی و restore مخزن در restic 0.19.1](https://restic.readthedocs.io/en/stable/045_working_with_repos.html)
- [Media type در Zabbix 7.0](https://www.zabbix.com/documentation/7.0/en/manual/config/notifications/media)
- [Email media در Zabbix 7.0](https://www.zabbix.com/documentation/7.0/en/manual/config/notifications/media/email)

</div>
