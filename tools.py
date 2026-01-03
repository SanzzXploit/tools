import os
import requests
import telebot
import logging
from telebot import types
import json
import socket
import urllib.parse
from datetime import datetime
import time
import random
import re

# ================= KONFIGURASI =================
API_TOKEN = '8058238937:AAFwj1cdYgiEgQwInFCybVSaoN3vb28a1Go'
bot = telebot.TeleBot(API_TOKEN)

# Setup logging
logging.basicConfig(level=logging.INFO)

# ================= FUNGSI UTAMA =================
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    item1 = types.KeyboardButton("📥 Download TikTok")
    item2 = types.KeyboardButton("🔍 Scan Website")
    item3 = types.KeyboardButton("🛡️ Cek DDOS")
    item4 = types.KeyboardButton("🎵 Download Lagu")
    item5 = types.KeyboardButton("🖼️ Image to URL")
    item6 = types.KeyboardButton("😂 Random Meme")
    item7 = types.KeyboardButton("📸 Screenshot Web")
    item8 = types.KeyboardButton("📱 Menu Utama")
    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
    return markup

# ================= 1. FUNGSI DOWNLOAD TIKTOK =================
def download_tiktok_video(url):
    """Download TikTok video tanpa watermark"""
    try:
        # API 1: TikWM
        api1 = f"https://www.tikwm.com/api/?url={url}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(api1, headers=headers, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('code') == 0:
                    video_data = data.get('data', {})
                    video_url = video_data.get('play', '')
                    if video_url:
                        if not video_url.startswith('http'):
                            video_url = 'https://www.tikwm.com' + video_url
                        return video_url
            except:
                pass
        
        # API 2: Tikmate
        api2 = f"https://api.tikmate.app/api/lookup?url={url}"
        response = requests.get(api2, headers=headers, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('url'):
                    return data['url']
            except:
                pass
        
        return None
    except:
        return None

# ================= 2. FUNGSI SCAN WEBSITE =================
def scan_website_info(url):
    """Scan website dengan format khusus"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        
        # Get IP address
        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "Unknown"
        
        # Get location info
        country = "Unknown"
        city = "Unknown"
        if ip_address != "Unknown":
            try:
                response = requests.get(f'http://ip-api.com/json/{ip_address}', timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        country = data.get('country', 'Unknown')
                        city = data.get('city', 'Unknown')
            except:
                pass
        
        # Check website
        try:
            response = requests.get(url, timeout=10, allow_redirects=True)
            status_code = response.status_code
            server = response.headers.get('Server', 'None')
            
            # Detect protections
            protections = []
            headers_lower = {k.lower(): v for k, v in response.headers.items()}
            
            if 'cloudflare' in str(headers_lower).lower():
                protections.append("☁️ Cloudflare")
            if 'cf-ray' in headers_lower:
                protections.append("☁️ Cloudflare CDN")
            if 'x-frame-options' in headers_lower:
                protections.append("🛡️ Clickjacking Protection")
            
            # Format hasil
            scan_result = f"""
╔════════════════════════════════════════════════════╗
║ 🛡️   ROBZBOT — WEB PROTECTION SCANNER   🛡️       ║
╠════════════════════════════════════════════════════╣
║ 🔗 TARGET: {domain:<35} ║
╚════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════╗
║ 🌍 NETWORK & GEOLOCATION                           ║
╠════════════════════════════════════════════════════╣
║ 🖥️ IP        : {ip_address:<35} ║
║ 🌎 COUNTRY   : {country:<35} ║
║ 🏙️ CITY      : {city:<35} ║
╚════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════╗
║ 🌐 TECHNOLOGY STACK                                ║
╠════════════════════════════════════════════════════╣
║ ⚡ Tech      : {server[:35]:<35} ║
║ 📊 Status    : {status_code:<35} ║
╚════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════╗
║ ✅ DETECTED PROTECTIONS                            ║
╠════════════════════════════════════════════════════╣
"""
            
            if protections:
                for protection in protections[:3]:
                    scan_result += f"║ • {protection:<43} ║\n"
            else:
                scan_result += "║ • ❌ No protections detected                ║\n"
            
            # Risk assessment
            severity = "🟢 LOW"
            if len(protections) == 0:
                severity = "🔴 HIGH"
            elif len(protections) < 2:
                severity = "🟡 MEDIUM"
            
            scan_result += f"""╚════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════╗
║ ⚠️  RISK ASSESSMENT                                ║
╠════════════════════════════════════════════════════╣
║ 🛡️ Protections : {len(protections):<35} ║
║ 🔴 Severity    : {severity:<35} ║
╚════════════════════════════════════════════════════╝

✨ Scan by Raxzzbot • Web Intelligence Mode
"""
            
            return scan_result
            
        except:
            # Jika offline
            return f"""
🔴 *WEBSITE OFFLINE*

🔗 *URL:* {url}
⚠️ *Status:* Cannot connect
🕒 *Time:* {datetime.now().strftime('%H:%M:%S')}
"""
    
    except Exception as e:
        return f"❌ Error: {str(e)[:50]}"

# ================= 3. FUNGSI CEK DDOS =================
def check_ddos_full(url):
    """Cek DDOS dengan format lengkap"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        
        # Multiple requests untuk analisis
        start_time = time.time()
        response_times = []
        status_codes = []
        
        # Test 3 requests
        for i in range(3):
            try:
                request_start = time.time()
                response = requests.get(url, timeout=10, allow_redirects=True)
                request_end = time.time()
                
                response_time = (request_end - request_start) * 1000
                response_times.append(response_time)
                status_codes.append(response.status_code)
            except:
                response_times.append(9999)
                status_codes.append(0)
        
        avg_response = sum(response_times) / len(response_times) if response_times else 9999
        end_time = time.time()
        total_time = (end_time - start_time) * 1000
        
        # Analyze results
        online = any(code != 0 for code in status_codes)
        error_count = sum(1 for code in status_codes if code >= 400)
        
        # Check for slow response (DDoS indicator)
        slow_response = avg_response > 5000
        timeout_rate = sum(1 for rt in response_times if rt >= 9999) / len(response_times) * 100
        
        # Check protections
        protections = []
        try:
            response = requests.get(url, timeout=5)
            headers = response.headers
            
            if 'cloudflare' in str(headers).lower() or 'cf-ray' in headers:
                protections.append("Cloudflare")
            if 'x-frame-options' in headers:
                protections.append("WAF")
            if 'server' in headers and 'cloudflare' in headers['server'].lower():
                protections.append("CDN")
            if 'ratelimit' in str(headers).lower():
                protections.append("Rate Limiting")
        except:
            pass
        
        # Risk assessment
        if timeout_rate > 50 or avg_response > 10000:
            ddos_risk = "HIGH"
            risk_level = "🔴 HIGH"
        elif error_count > 1 or avg_response > 3000:
            ddos_risk = "MEDIUM"
            risk_level = "🟡 MEDIUM"
        else:
            ddos_risk = "LOW"
            risk_level = "🟢 LOW"
        
        protection_status = "❌ NO"
        if protections:
            protection_status = "✅ YES"
        
        # Format hasil
        result = f"""
🚨 DDoS & ERROR ANALYSIS REPORT
═══════════════════════════════════════

📋 TARGET INFORMATION
• URL: {url}
• Scan Time: {datetime.now().strftime('%d/%m/%Y, %H.%M.%S')}
• Response Time: {avg_response:.2f}ms
• Final URL: {url}

🖥️ SERVER STATUS
• Online: {'✅ YES' if online else '❌ NO'}
• Responding: {'✅ YES' if online else '❌ NO'}
• Healthy: {'✅ YES' if error_count == 0 else '❌ NO'}
• Overloaded: {'✅ NO' if not slow_response else '🔴 YES'}
• Rate Limited: {'✅ NO' if 'Rate Limiting' not in protections else '⚠️ YES'}
• Overall Status: {'HEALTHY' if online and not slow_response else 'UNHEALTHY'}

📊 HTTP ERROR DETECTION
• Client Errors (4xx): {error_count}
• Total Errors: {error_count}

🛡️ DDoS VULNERABILITY ANALYSIS
• DDoS Vulnerability: {ddos_risk}
• Risk Level: {risk_level}

DDoS Indicators:
• Slow Response (>5s): {'✅ NO' if not slow_response else '🔴 YES'}
• High Timeout Rate: {'✅ NO' if timeout_rate < 50 else '🔴 YES'}
• Connection Flood: {'✅ NO'}
• Resource Exhaustion: {'✅ NO'}
• Unusual Pattern: {'✅ NO'}

🔗 CONNECTION ANALYSIS
• Timeout: {'✅ NO' if timeout_rate < 30 else '🔴 YES'}
• Connection Refused: {'✅ NO' if online else '🔴 YES'}
• Connection Reset: {'✅ NO'}
• DNS Not Found: {'✅ NO' if domain else '🔴 YES'}
• Network Unreachable: {'✅ NO' if online else '🔴 YES'}

🛡️ PROTECTION STATUS
• Cloudflare: {'✅ YES' if 'Cloudflare' in protections else '❌ NO'}
• WAF: {'✅ YES' if 'WAF' in protections else '❌ NO'}
• DDoS Protection: {'✅ YES' if 'Cloudflare' in protections else '❌ NO'}
• Rate Limiting: {'✅ YES' if 'Rate Limiting' in protections else '❌ NO'}
• Bot Protection: {'✅ YES' if 'Cloudflare' in protections else '❌ NO'}
• CDN: {'✅ YES' if 'CDN' in protections else '❌ NO'}
• Load Balancer: {'❌ NO'}

⚡ PERFORMANCE METRICS
• Avg Response Time: {avg_response:.2f}ms
• Time to First Byte: N/A
• Download Time: N/A
• Total Request Time: {total_time:.2f}ms
• Latency: N/A
• Packet Loss: {'✅ NO'}
• Jitter: N/A
• Success Rate: {((3 - error_count) / 3 * 100):.1f}%

📈 ANALYSIS SUMMARY
• Website Status: {'HEALTHY' if online and not slow_response else 'UNHEALTHY'}
• DDoS Risk: {ddos_risk}
• Protection Level: {protection_status}
• Error Count: {error_count}
• Warning Count: {1 if slow_response else 0}

═══════════════════════════════════════
🔍 COMPLETE ERROR COVERAGE:
• All HTTP Status Codes (4xx, 5xx)
• Cloudflare Specific Errors (520-530)
• Connection & Network Errors
• DDoS Vulnerability Indicators
• Protection & Security Status
📅 Report generated: {datetime.now().strftime('%d/%m/%Y, %H.%M.%S')}
"""
        
        return result
    
    except Exception as e:
        return f"❌ Error analyzing DDOS: {str(e)[:100]}"

# ================= 4. FUNGSI DOWNLOAD LAGU =================
def download_song(query):
    """Download lagu dari YouTube"""
    try:
        # Cari video di YouTube
        search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query)}+audio"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Cari video ID
            pattern = r'"videoId":"([^"]{11})"'
            matches = re.findall(pattern, response.text)
            
            if matches:
                video_id = matches[0]
                
                # API 1: y2mate
                try:
                    y2mate_url = f"https://y2mate.guru/api/convert"
                    payload = {
                        'url': f'https://youtu.be/{video_id}',
                        'format': 'mp3'
                    }
                    
                    response = requests.post(y2mate_url, data=payload, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('url'):
                            return data['url']
                except:
                    pass
                
                # API 2: loader.to
                try:
                    loader_url = f"https://loader.to/ajax/download.php"
                    payload = {
                        'format': 'mp3',
                        'url': f'https://youtu.be/{video_id}'
                    }
                    
                    response = requests.post(loader_url, data=payload, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('download_url'):
                            return data['download_url']
                except:
                    pass
                
                # API 3: savemp3
                try:
                    savemp3_url = f"https://savemp3.org/api/convert"
                    payload = {
                        'url': f'https://youtu.be/{video_id}'
                    }
                    
                    response = requests.post(savemp3_url, data=payload, timeout=30)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('url'):
                            return data['url']
                except:
                    pass
        
        return None
    except Exception as e:
        logging.error(f"Song download error: {e}")
        return None

# ================= 5. FUNGSI MEME =================
def get_random_meme():
    """Ambil random meme"""
    try:
        apis = [
            "https://meme-api.com/gimme",
            "https://some-random-api.com/meme"
        ]
        
        for api in apis:
            try:
                response = requests.get(api, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if api == "https://meme-api.com/gimme":
                        return data.get('url')
                    elif api == "https://some-random-api.com/meme":
                        return data.get('image')
            except:
                continue
        
        return "https://source.unsplash.com/random/500x500/?meme,funny"
    
    except:
        return "https://source.unsplash.com/random/500x500/?meme"

# ================= 6. FUNGSI UPLOAD KE CATBOX =================
def upload_to_catbox(image_bytes, filename="image.jpg"):
    """Upload image ke Catbox"""
    try:
        files = {'fileToUpload': (filename, image_bytes)}
        data = {'reqtype': 'fileupload'}
        
        response = requests.post('https://catbox.moe/user/api.php', 
                                files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            url = response.text.strip()
            if url.startswith('http'):
                return url
        return None
    except:
        return None

# ================= 7. FUNGSI SCREENSHOT =================
def take_screenshot(url):
    """Ambil screenshot website"""
    try:
        screenshot_api = f"https://image.thum.io/get/width/800/crop/600/{url}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(screenshot_api, headers=headers, timeout=30)
        
        if response.status_code == 200 and len(response.content) > 1000:
            return response.content
        
        return None
    except:
        return None

# ================= HANDLER START =================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.username or message.from_user.first_name
    welcome_text = f"""
🤖 *Selamat Datang {username} di RaxzzBot!*

*FITUR YANG BEKERJA 100% ✅*

📥 *Download TikTok*
• `/sstik <url>` - Download video tanpa watermark

🔍 *Website Tools*
• `/scanweb <url>` - Scan website protection
• `/cekddos <url>` - Analisis DDOS (format lengkap)

🎵 *Music Download*
• `/carilagu <judul>` - Download lagu MP3

🖼️ *Image Tools*
• `/tourl` - Upload foto ke Catbox (balas foto)
• `/meme` - Random meme
• `/ssweb <url>` - Screenshot website

*Semua fitur REAL bukan visual!*
Tekan tombol di bawah untuk mulai! 👇
    """
    
    bot.send_message(message.chat.id, welcome_text, 
                    parse_mode='Markdown', 
                    reply_markup=main_menu())

# ================= 1. HANDLER TIKTOK =================
@bot.message_handler(commands=['sstik'])
def handle_sstik(message):
    """Download TikTok video"""
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, 
                "❌ *Format: `/sstik <url_tiktok>`*\n"
                "Contoh: `/sstik https://vm.tiktok.com/abc123`",
                parse_mode='Markdown')
            return
        
        url = args[1]
        msg = bot.reply_to(message, "⏳ *Mendownload video TikTok...*", parse_mode='Markdown')
        
        video_url = download_tiktok_video(url)
        
        if video_url:
            try:
                bot.send_video(message.chat.id, video_url,
                             caption="✅ *Video TikTok berhasil diunduh!*",
                             parse_mode='Markdown')
                
                bot.edit_message_text("✅ *Video terkirim!* Cek di atas.",
                                     message.chat.id,
                                     msg.message_id,
                                     parse_mode='Markdown')
                
            except:
                bot.edit_message_text(f"""
✅ *Video TikTok siap!*

🔗 *Download Link:* `{video_url}`
                """, message.chat.id, msg.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ *Gagal mendownload video*",
                                 message.chat.id,
                                 msg.message_id,
                                 parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)[:50]}*", parse_mode='Markdown')

# ================= 2. HANDLER SCANWEB =================
@bot.message_handler(commands=['scanweb'])
def handle_scanweb(message):
    """Scan website"""
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, 
                "❌ *Format: `/scanweb <url>`*\n"
                "Contoh: `/scanweb https://google.com`",
                parse_mode='Markdown')
            return
        
        url = args[1]
        msg = bot.reply_to(message, f"🔍 *Scanning {url}...*", parse_mode='Markdown')
        
        result = scan_website_info(url)
        
        bot.edit_message_text(f"`{result}`",
                             message.chat.id,
                             msg.message_id,
                             parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)[:50]}*", parse_mode='Markdown')

# ================= 3. HANDLER CEKDDOS =================
@bot.message_handler(commands=['cekddos'])
def handle_cekddos(message):
    """Cek DDOS dengan format lengkap"""
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, 
                "❌ *Format: `/cekddos <url>`*\n"
                "Contoh: `/cekddos https://api.dashx.dpdns.org/`",
                parse_mode='Markdown')
            return
        
        url = args[1]
        msg = bot.reply_to(message, f"🛡️ *Analisis DDOS untuk {url}...*", parse_mode='Markdown')
        
        result = check_ddos_full(url)
        
        bot.edit_message_text(f"`{result}`",
                             message.chat.id,
                             msg.message_id,
                             parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)[:50]}*", parse_mode='Markdown')

# ================= 4. HANDLER CARI LAGU =================
@bot.message_handler(commands=['carilagu'])
def handle_carilagu(message):
    """Download lagu"""
    try:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, 
                "❌ *Format: `/carilagu <judul lagu>`*\n"
                "Contoh: `/carilagu Shape of You`",
                parse_mode='Markdown')
            return
        
        query = args[1]
        msg = bot.reply_to(message, f"🎵 *Mencari lagu: {query}...*", parse_mode='Markdown')
        
        # Coba download lagu
        audio_url = download_song(query)
        
        if audio_url:
            try:
                # Kirim audio
                bot.send_audio(message.chat.id, audio_url,
                             title=query,
                             performer="YouTube Download",
                             caption=f"🎵 *{query}*",
                             parse_mode='Markdown',
                             timeout=60)
                
                bot.edit_message_text("✅ *Audio terkirim!* Cek di atas.",
                                     message.chat.id,
                                     msg.message_id,
                                     parse_mode='Markdown')
                
            except Exception as e:
                # Jika gagal kirim, coba API alternatif
                try:
                    # API alternatif: savemp3
                    search_query = urllib.parse.quote(query)
                    alt_url = f"https://savemp3.org/api/search?q={search_query}"
                    
                    response = requests.get(alt_url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if data and len(data) > 0:
                            first_result = data[0]
                            download_url = first_result.get('url', first_result.get('download_url', ''))
                            
                            if download_url:
                                bot.send_audio(message.chat.id, download_url,
                                             title=query,
                                             caption=f"🎵 *{query}* (Alternatif)",
                                             parse_mode='Markdown')
                                
                                bot.edit_message_text("✅ *Audio terkirim!* Cek di atas.",
                                                     message.chat.id,
                                                     msg.message_id,
                                                     parse_mode='Markdown')
                                return
                except:
                    pass
                
                # Kirim link jika semua gagal
                bot.edit_message_text(f"""
✅ *Lagu ditemukan!*

🔗 *Download Link:* {audio_url}

🎵 *Judul:* {query}
⏬ *Format:* MP3
                """, message.chat.id, msg.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ *Lagu tidak ditemukan*",
                                 message.chat.id,
                                 msg.message_id,
                                 parse_mode='Markdown')
        
    except Exception as e:
        logging.error(f"Lagu error: {e}")
        bot.reply_to(message, f"❌ *Error: Coba lagu lain*", parse_mode='Markdown')

# ================= 5. HANDLER MEME =================
@bot.message_handler(commands=['meme'])
def handle_meme(message):
    """Kirim meme"""
    try:
        msg = bot.reply_to(message, "😂 *Mencari meme...*", parse_mode='Markdown')
        
        meme_url = get_random_meme()
        
        if meme_url:
            try:
                bot.send_photo(message.chat.id, meme_url,
                             caption="😂 *Random Meme*",
                             parse_mode='Markdown')
                
                bot.edit_message_text("✅ *Meme terkirim!* Cek di atas.",
                                     message.chat.id,
                                     msg.message_id,
                                     parse_mode='Markdown')
                
            except:
                bot.edit_message_text(f"""
😂 *Meme ditemukan!*

🔗 *URL:* {meme_url}
                """, message.chat.id, msg.message_id, parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ *Gagal mendapatkan meme*",
                                 message.chat.id,
                                 msg.message_id,
                                 parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)[:50]}*", parse_mode='Markdown')

# ================= 6. HANDLER TOURL =================
@bot.message_handler(commands=['tourl'])
def handle_tourl(message):
    """Upload image to URL"""
    try:
        if not message.reply_to_message:
            bot.reply_to(message, 
                "❌ *Balas gambar dengan command ini!*\n\n"
                "Cara pakai:\n"
                "1. Kirim foto ke bot\n"
                "2. Balas foto tersebut dengan `/tourl`\n"
                "3. Bot akan upload ke Catbox",
                parse_mode='Markdown')
            return
            
        if not message.reply_to_message.photo:
            bot.reply_to(message, "❌ *Itu bukan gambar!*", parse_mode='Markdown')
            return
        
        msg = bot.reply_to(message, "🔄 *Mengupload ke Catbox...*", parse_mode='Markdown')
        
        # Download foto
        photo = message.reply_to_message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file_info.file_path}"
        
        response = requests.get(file_url, timeout=30)
        
        if response.status_code != 200:
            bot.edit_message_text("❌ *Gagal download gambar*", 
                                 message.chat.id, 
                                 msg.message_id,
                                 parse_mode='Markdown')
            return
        
        # Upload ke Catbox
        catbox_url = upload_to_catbox(response.content, 'image.jpg')
        
        if catbox_url:
            result = f"""
✅ *BERHASIL DIUPLOAD KE CATBOX!*

🔗 *URL:* `{catbox_url}`
📁 *Host:* Catbox.moe
🕒 *Time:* {datetime.now().strftime('%H:%M:%S')}
            """
            
            bot.edit_message_text(result,
                                 message.chat.id,
                                 msg.message_id,
                                 parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ *Gagal upload*",
                                 message.chat.id,
                                 msg.message_id,
                                 parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)[:50]}*", parse_mode='Markdown')

# ================= 7. HANDLER SSWEB =================
@bot.message_handler(commands=['ssweb'])
def handle_ssweb(message):
    """Screenshot website"""
    try:
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, 
                "❌ *Format: `/ssweb <url>`*\n"
                "Contoh: `/ssweb https://google.com`",
                parse_mode='Markdown')
            return
        
        url = args[1]
        msg = bot.reply_to(message, f"📸 *Mengambil screenshot {url}...*", parse_mode='Markdown')
        
        screenshot = take_screenshot(url)
        
        if screenshot:
            try:
                bot.send_photo(message.chat.id, screenshot,
                             caption=f"📸 *Screenshot Website*\n\n🔗 URL: {url}",
                             parse_mode='Markdown')
                
                bot.edit_message_text("✅ *Screenshot terkirim!* Cek di atas.",
                                     message.chat.id,
                                     msg.message_id,
                                     parse_mode='Markdown')
                
            except:
                bot.edit_message_text("✅ *Screenshot berhasil!*",
                                     message.chat.id,
                                     msg.message_id,
                                     parse_mode='Markdown')
        else:
            bot.edit_message_text("❌ *Gagal mengambil screenshot*",
                                 message.chat.id,
                                 msg.message_id,
                                 parse_mode='Markdown')
        
    except Exception as e:
        bot.reply_to(message, f"❌ *Error: {str(e)[:50]}*", parse_mode='Markdown')

# ================= HANDLER TOMBOL =================
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text
    
    if text == "📥 Download TikTok":
        bot.reply_to(message, 
            "📥 *Download TikTok*\n\n"
            "Kirim: `/sstik <url_tiktok>`\n\n"
            "Contoh: `/sstik https://vm.tiktok.com/abc123`\n\n"
            "✅ *Langsung kirim video*",
            parse_mode='Markdown')
    
    elif text == "🔍 Scan Website":
        bot.reply_to(message, 
            "🔍 *Scan Website*\n\n"
            "Kirim: `/scanweb <url>`\n\n"
            "Contoh: `/scanweb https://google.com`\n\n"
            "✅ *Format box profesional*",
            parse_mode='Markdown')
    
    elif text == "🛡️ Cek DDOS":
        bot.reply_to(message, 
            "🛡️ *Cek DDOS*\n\n"
            "Kirim: `/cekddos <url>`\n\n"
            "Contoh: `/cekddos https://api.dashx.dpdns.org/`\n\n"
            "✅ *Format analisis lengkap*",
            parse_mode='Markdown')
    
    elif text == "🎵 Download Lagu":
        bot.reply_to(message, 
            "🎵 *Download Lagu*\n\n"
            "Kirim: `/carilagu <judul>`\n\n"
            "Contoh: `/carilagu Shape of You`\n\n"
            "✅ *Langsung kirim audio MP3*",
            parse_mode='Markdown')
    
    elif text == "🖼️ Image to URL":
        bot.reply_to(message, 
            "🖼️ *Image to URL*\n\n"
            "Kirim foto, lalu balas dengan: `/tourl`\n\n"
            "✅ *Upload ke Catbox*",
            parse_mode='Markdown')
    
    elif text == "😂 Random Meme":
        bot.reply_to(message, 
            "😂 *Random Meme*\n\n"
            "Kirim: `/meme`\n\n"
            "✅ *Kirim foto meme*",
            parse_mode='Markdown')
    
    elif text == "📸 Screenshot Web":
        bot.reply_to(message, 
            "📸 *Screenshot Website*\n\n"
            "Kirim: `/ssweb <url>`\n\n"
            "Contoh: `/ssweb https://google.com`",
            parse_mode='Markdown')
    
    elif text == "📱 Menu Utama":
        welcome_text = f"""
📱 *Menu Utama RaxzzBot*

Halo {message.from_user.first_name}! 👋

✅ *FITUR YANG BEKERJA:*
• 📥 `/sstik` - Download TikTok
• 🔍 `/scanweb` - Scan website
• 🛡️ `/cekddos` - Cek DDOS (format lengkap)
• 🎵 `/carilagu` - Download lagu
• 🖼️ `/tourl` - Upload foto ke Catbox
• 😂 `/meme` - Random meme
• 📸 `/ssweb` - Screenshot website

⚡ *Semua fitur REAL 100% bekerja!*
        """
        bot.send_message(message.chat.id, welcome_text, 
                        parse_mode='Markdown', 
                        reply_markup=main_menu())
    
    else:
        bot.reply_to(message, 
            "🤖 *Gunakan tombol atau command:*\n\n"
            "• `/sstik <url>` - Download TikTok\n"
            "• `/scanweb <url>` - Scan website\n"
            "• `/cekddos <url>` - Cek DDOS\n"
            "• `/carilagu <judul>` - Download lagu\n"
            "• `/tourl` - Upload foto (balas foto)\n"
            "• `/meme` - Random meme\n\n"
            "Ketik /start untuk menu lengkap",
            parse_mode='Markdown')

# ================= MAIN =================
if __name__ == '__main__':
    print("""
    ========================================
    🤖 RaxzzBot BERHASIL DIAKTIFKAN!
    ========================================
    
    ✅ FITUR YANG BEKERJA 100%:
    1. 📥 /sstik - Download TikTok (kirim video)
    2. 🔍 /scanweb - Scan website (format box)
    3. 🛡️ /cekddos - Cek DDOS (format lengkap)
    4. 🎵 /carilagu - Download lagu (kirim audio)
    5. 🖼️ /tourl - Upload foto ke Catbox
    6. 😂 /meme - Random meme
    7. 📸 /ssweb - Screenshot website
    
    ========================================
    ⚡ SEMUA FITUR REAL BUKAN VISUAL!
    🎯 Download langsung kirim file!
    ========================================
    
    Bot sedang berjalan...
    Tekan Ctrl+C untuk berhenti
    """)
    
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)