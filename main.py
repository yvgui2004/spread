"""
Stereo Audio Channel Splitter / 立体声左右声道分离工具
=====================================================
Extract left/right channels into separate stereo files.
FFmpeg pan filter + customtkinter + Impeccable dual-theme.
"""

import os, sys, json, subprocess, threading, time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Dict, List

import customtkinter as ctk
from PIL import Image

# Windows 下用 pythonw 启动时,子进程会弹出控制台窗口;此标志可隐藏它
CREATE_NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)

# ═══════════════════════════════════════════════════════
DARK  = {"bg":"#0F1117","surface":"#161A22","border":"#252A35","fg":"#E8ECF1",
         "fg2":"#8B949E","accent":"#5B8DEF","danger":"#F14C4C","success":"#3FB950","input":"#0B0E14"}
LIGHT = {"bg":"#F6F8FA","surface":"#FFFFFF","border":"#D0D7DE","fg":"#1A1C23",
         "fg2":"#656D76","accent":"#4263EB","danger":"#CF222E","success":"#1A7F37","input":"#FFFFFF"}

W, H = 1024, 723; MIN_W, MIN_H = 1024, 723
FONT  = ("Microsoft YaHei",12); FONT_S = ("Microsoft YaHei",11)
FONT_B = ("Microsoft YaHei",12,"bold"); FONT_T = ("Microsoft YaHei",14,"bold")
MONO  = ("Cascadia Code",10)

CODEC_MAP = {'mp3':'libmp3lame','mp3float':'libmp3lame','aac':'aac','opus':'libopus',
    'vorbis':'libvorbis','flac':'flac','alac':'alac','wavpack':'wavpack',
    'pcm_s16le':'pcm_s16le','pcm_s24le':'pcm_s24le','pcm_s32le':'pcm_s32le',
    'pcm_f32le':'pcm_f32le','pcm_f32be':'pcm_f32be','pcm_s16be':'pcm_s16be',
    'pcm_s24be':'pcm_s24be','pcm_u8':'pcm_u8','wmav2':'wmav2','wmav1':'wmav1',
    'ac3':'ac3','eac3':'eac3','dts':'dts'}
LOSSLESS = frozenset({'flac','alac','wavpack','pcm_s16le','pcm_s24le','pcm_s32le',
                       'pcm_f32le','pcm_f32be','pcm_s16be','pcm_s24be','pcm_u8'})
MEDIA_EXTS = ('.mp3','.wav','.flac','.aac','.m4a','.ogg','.opus','.wma',
              '.mp4','.mkv','.avi','.mov','.webm','.flv','.wmv')
VIDEO_EXTS = frozenset({'.mp4','.mkv','.avi','.mov','.webm','.flv','.wmv'})
CODEC_EXT = {'aac':'.m4a','mp3':'.mp3','libmp3lame':'.mp3','opus':'.opus',
    'libopus':'.opus','vorbis':'.ogg','libvorbis':'.ogg','flac':'.flac',
    'pcm_s16le':'.wav','pcm_s24le':'.wav','pcm_s32le':'.wav','pcm_f32le':'.wav',
    'alac':'.m4a','wmav2':'.wma','wmav1':'.wma','ac3':'.ac3','eac3':'.eac3','dts':'.dts'}

# ═══════════════════════════════════════════════════════
T = {
'zh': {
    'title':"立体声左右声道分离工具",
    'select_file':"📂 选择文件",
    'btn_select':"选择文件...",
    'btn_batch':"批量添加",
    'btn_clear':"清空",
    'btn_theme_light':"☀ 亮色",
    'btn_theme_dark':"🌙 暗色",
    'btn_lang':"EN",
    'file_info':"📋 文件信息",
    'fn':'文件名','fmt':'格式','codec_l':'编码器','br':'比特率','sr':'采样率','ch':'声道','dur':'时长',
    'output':"📁 输出设置",
    'same_dir':"与源文件同目录",
    'btn_browse':"浏览...",
    'progress':"📊 处理进度",
    'ready':"就绪 — 请选择音频文件",
    'log':"📝 处理日志",
    'btn_clear_log':"清空",
    'btn_open_dir':"📁 打开输出目录",
    'btn_cancel':"取消",
    'btn_start':"▶ 开始分离",
    'btn_swap':"🔄 声道反转",
    'no_files':"  暂无文件，请添加音频/视频文件\n",
    'dlog_read':"读取失败",
    'dlog_cant_read':"无法读取:\n",
    'dlog_non_stereo':"非立体声",
    'dlog_channels':"声道数: {}，无法分离\n",
    'dlog_pick_file':"选择音频/视频文件",
    'dlog_pick_batch':"批量添加媒体文件",
    'dlog_pick_dir':"选择输出目录",
    'dlog_warn':"输出目录无效",
    'dlog_warn_msg':"请选择有效的输出目录",
    'dlog_info':"提示",
    'dlog_info_add':"请先添加媒体文件",
    'dlog_overwrite':"文件覆盖确认",
    'dlog_overwrite_msg':"以下 {} 个文件已存在，处理时将覆盖:\n\n",
    'dlog_overwrite_more':"\n  ... 还有 {} 个",
    'dlog_overwrite_ask':"\n\n是否继续？",
    'dlog_yes':"继续",
    'dlog_no':"取消",
    'dlog_close':"确认",
    'dlog_close_ask':"正在处理中，确定退出？",
    'processing':"处理中...",
    'preparing':"正在准备...",
    'cancelling':"⏹ 正在取消...",
    'cancelled_clean':"  ⏹ 已取消并清理",
    'done_ok':"  ✅ 完成",
    'done_fail':"  ❌ 失败 (code {})",
    'done_err':"  ❌ {}",
    'status_cancelled':"已取消 — 成功 {}, 失败 {}",
    'status_done':"完成 — 成功 {} 个, 失败 {} 个",
    'summary':"处理{}。成功: {}, 失败: {}",
    'summary_cancelled':"已取消",
    'summary_done':"完成",
    'failed_file':"  失败: {}",
    'dir_not_exist':"输出目录不存在",
    'missing_ffmpeg':"未检测到 FFmpeg。\n下载: https://ffmpeg.org/download.html",
    'media_filter':"媒体文件",
    'all_files':"所有文件",
},
'en': {
    'title':"Stereo Channel Splitter",
    'select_file':"📂 Select Files",
    'btn_select':"Select File...",
    'btn_batch':"Batch Add",
    'btn_clear':"Clear",
    'btn_theme_light':"☀ Light",
    'btn_theme_dark':"🌙 Dark",
    'btn_lang':"中",
    'file_info':"📋 File Info",
    'fn':'Filename','fmt':'Format','codec_l':'Codec','br':'Bitrate','sr':'Sample Rate','ch':'Channels','dur':'Duration',
    'output':"📁 Output",
    'same_dir':"Same as source",
    'btn_browse':"Browse...",
    'progress':"📊 Progress",
    'ready':"Ready — select a media file",
    'log':"📝 Log",
    'btn_clear_log':"Clear",
    'btn_open_dir':"📁 Open Output",
    'btn_cancel':"Cancel",
    'btn_start':"▶ Start Split",
    'btn_swap':"🔄 Swap Channels",
    'no_files':"  No files. Click Select File or Batch Add.\n",
    'dlog_read':"Read Error",
    'dlog_cant_read':"Cannot read:\n",
    'dlog_non_stereo':"Not Stereo",
    'dlog_channels':"Channel count: {}, cannot split\n",
    'dlog_pick_file':"Select Media File",
    'dlog_pick_batch':"Batch Add Media Files",
    'dlog_pick_dir':"Select Output Directory",
    'dlog_warn':"Invalid Output",
    'dlog_warn_msg':"Please select a valid output directory",
    'dlog_info':"Info",
    'dlog_info_add':"Please add media files first",
    'dlog_overwrite':"Overwrite Confirm",
    'dlog_overwrite_msg':"The following {} file(s) already exist and will be overwritten:\n\n",
    'dlog_overwrite_more':"\n  ... and {} more",
    'dlog_overwrite_ask':"\n\nContinue?",
    'dlog_yes':"Continue",
    'dlog_no':"Cancel",
    'dlog_close':"Confirm",
    'dlog_close_ask':"Processing in progress. Quit?",
    'processing':"Processing...",
    'preparing':"Preparing...",
    'cancelling':"⏹ Cancelling...",
    'cancelled_clean':"  ⏹ Cancelled, cleaned up",
    'done_ok':"  ✅ Done",
    'done_fail':"  ❌ Failed (code {})",
    'done_err':"  ❌ {}",
    'status_cancelled':"Cancelled — {} ok, {} failed",
    'status_done':"Done — {} succeeded, {} failed",
    'summary':"{} — ok: {}, fail: {}",
    'summary_cancelled':"Cancelled",
    'summary_done':"Done",
    'failed_file':"  Failed: {}",
    'dir_not_exist':"Output directory does not exist",
    'missing_ffmpeg':"FFmpeg not found.\nDownload: https://ffmpeg.org/download.html",
    'media_filter':"Media Files",
    'all_files':"All Files",
}}

# ═══════════════════════════════════════════════════════

def probe(fp):
    try:
        r = subprocess.run(['ffprobe','-v','quiet','-print_format','json',
            '-show_format','-show_streams',fp],
            capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=20,
            creationflags=CREATE_NO_WINDOW)
        if r.returncode: return None
        d = json.loads(r.stdout)
        au = next((s for s in d.get('streams',[]) if s.get('codec_type')=='audio'),None)
        if not au: return None
        fmt = d.get('format',{})
        return {'codec':au.get('codec_name','?'),'codec_long':au.get('codec_long_name','?'),
            'sample_rate':int(au.get('sample_rate',0)),'channels':int(au.get('channels',0)),
            'channel_layout':au.get('channel_layout','?'),
            'bit_rate':int(au.get('bit_rate') or fmt.get('bit_rate') or '0'),
            'duration':float(au.get('duration') or fmt.get('duration') or '0'),
            'format':(fmt.get('format_name') or '?').split(',')[0].upper(),
            'filename':os.path.basename(fp),'filepath':fp,'ext':os.path.splitext(fp)[1].lower()}
    except: return None

def build_cmd(info, out_dir):
    base = os.path.splitext(info['filename'])[0]
    out_ext = CODEC_EXT.get(info['codec'],info['ext']) if info['ext'] in VIDEO_EXTS else info['ext']
    lp = os.path.join(out_dir,f"{base}_L{out_ext}")
    rp = os.path.join(out_dir,f"{base}_R{out_ext}")
    enc = CODEC_MAP.get(info['codec'],info['codec'])
    sr,br,ls = info['sample_rate'],info['bit_rate'],info['codec'] in LOSSLESS
    cmd = ['ffmpeg','-hide_banner','-loglevel','warning','-progress','pipe:2','-nostats',
        '-i',info['filepath'],'-filter_complex',
        '[0:a]pan=stereo|c0=c0|c1=0*c0[left];[0:a]pan=stereo|c0=0*c1|c1=c1[right]']
    for tag,out in [('[left]',lp),('[right]',rp)]:
        cmd += ['-map',tag,'-c:a',enc]
        if sr>0: cmd += ['-ar',str(sr)]
        if br>0 and not ls: cmd += ['-b:a',str(br)]
        cmd.append(out)
    return cmd,lp,rp

def build_swap_cmd(info, out_dir):
    base = os.path.splitext(info['filename'])[0]
    out_ext = CODEC_EXT.get(info['codec'],info['ext']) if info['ext'] in VIDEO_EXTS else info['ext']
    out = os.path.join(out_dir,f"{base}_swap{out_ext}")
    enc = CODEC_MAP.get(info['codec'],info['codec'])
    sr,br,ls = info['sample_rate'],info['bit_rate'],info['codec'] in LOSSLESS
    cmd = ['ffmpeg','-hide_banner','-loglevel','warning','-progress','pipe:2','-nostats',
        '-i',info['filepath'],'-map','0:a','-af','pan=stereo|c0=c1|c1=c0','-c:a',enc]
    if sr>0: cmd += ['-ar',str(sr)]
    if br>0 and not ls: cmd += ['-b:a',str(br)]
    cmd.append(out)
    return cmd,out

def fmt_dur(sec): return f"{int(sec//60)}:{int(sec%60):02d}" if sec>0 else '--:--'
def fmt_br(b): return f"{b//1000}kbps" if b>=1000 else f"{b}bps"

# ═══════════════════════════════════════════════════════

class App:
    def __init__(self):
        self.files:List[Dict]=[]; self.running=False; self.cancelled=False
        self.proc=None; self.same_dir=True; self.custom_dir=""; self.mode='split'

        self._cfg = Path(__file__).parent/"config.json"
        cfg = self._load_cfg()
        self.dark = cfg.get('dark',True); self.lang = cfg.get('lang','zh')
        self.c = DARK if self.dark else LIGHT

        ctk.set_appearance_mode("dark" if self.dark else "light")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title(self._t('title'))
        self.root.geometry(f"{W}x{H}"); self.root.minsize(MIN_W,MIN_H)
        self.root.configure(fg_color=self.c["bg"])
        self._ico = Path(__file__).parent/"spread.ico"
        self._ico_img = None
        if self._ico.exists():
            try: self.root.iconbitmap(str(self._ico))
            except Exception: pass
            try:
                _pil = Image.open(self._ico).convert("RGBA")
                self._ico_img = ctk.CTkImage(light_image=_pil,dark_image=_pil,size=(24,24))
            except Exception: self._ico_img = None
        self._center()
        self.root.protocol("WM_DELETE_WINDOW",self._close)
        self._build()
        if not self.dark: self._apply_theme()
        self.root.mainloop()

    def _t(self,key,*args):
        s = T[self.lang].get(key,key)
        return s.format(*args) if args else s

    def _load_cfg(self):
        try:
            if self._cfg.exists():
                with open(self._cfg,'r',encoding='utf-8') as f: return json.load(f)
        except: pass
        return {}

    def _save_cfg(self):
        try:
            with open(self._cfg,'w',encoding='utf-8') as f:
                json.dump({'dark':self.dark,'lang':self.lang},f)
        except: pass

    # ═══════════════════════════════════════════════════
    # 主题
    # ═══════════════════════════════════════════════════

    def _toggle_theme(self):
        if getattr(self,'_animating',False): return
        self._animating = True
        def fade_out(step=5):
            if step>0: self.root.attributes('-alpha',step/5); self.root.after(20,lambda s=step:fade_out(s-1))
            else:
                self.root.attributes('-alpha',0.0)
                self.dark = not self.dark; self.c = DARK if self.dark else LIGHT
                self._save_cfg()
                ctk.set_appearance_mode("dark" if self.dark else "light")
                self._apply_theme()
                self.root.update_idletasks(); self.root.update(); self.root.update_idletasks()
                fade_in(1)
        def fade_in(step=1):
            if step<=5: self.root.attributes('-alpha',step/5); self.root.after(20,lambda s=step:fade_in(s+1))
            else: self.root.attributes('-alpha',1.0); self._animating=False
        fade_out()

    def _apply_theme(self):
        c = self.c
        self.root.configure(fg_color=c["bg"])
        for card in self.cards: card.configure(fg_color=c["surface"],border_color=c["border"])
        for box in self.boxes: box.configure(fg_color=c["input"])
        for tw in self._text_widgets: tw.configure(bg=c["input"],fg=c["fg"])
        self.info_frame.configure(fg_color=c["input"])
        self.out_entry.configure(fg_color=c["input"],text_color=c["fg"],border_color=c["border"])
        self.pbar.configure(progress_color=c["accent"],fg_color=c["border"])
        self.same_sw.configure(text_color=c["fg"],progress_color=c["accent"],button_color=c["accent"])
        for lbl in self.all_labels:
            try: lbl.configure(text_color=c["fg2"])
            except: pass
        for lbl in self.info_lbls.values(): lbl.configure(text_color=c["fg"])
        btn_bg = c["accent"] if not self.dark else c["border"]
        for btn in self._neutral_btns: btn.configure(fg_color=btn_bg,hover_color=btn_bg,text_color="#fff")
        self.btn_theme.configure(text=self._t('btn_theme_light') if self.dark else self._t('btn_theme_dark'))
        self.btn_cancel.configure(fg_color=c["danger"],hover_color=c["danger"],text_color="#fff")
        self._refresh()

    # ═══════════════════════════════════════════════════
    # 语言切换
    # ═══════════════════════════════════════════════════

    def _toggle_lang(self):
        self.lang = 'en' if self.lang=='zh' else 'zh'
        self._save_cfg()
        self._update_texts()

    def _update_texts(self):
        t = self._t
        self.root.title(t('title'))
        for lbl,key in self._title_labels: lbl.configure(text=t(key))
        for btn,key in self._btn_labels: btn.configure(text=t(key))
        for lbl,key in self._info_labels: lbl.configure(text=f"{t(key)}：")
        self.same_sw.configure(text=t('same_dir'))
        self.status_lbl.configure(text=t('ready'))
        self.btn_theme.configure(text=t('btn_theme_light') if self.dark else t('btn_theme_dark'))
        self._refresh()

    # ═══════════════════════════════════════════════════
    # UI
    # ═══════════════════════════════════════════════════

    def _build(self):
        t = self._t; c = self.c
        self.cards=[]; self.boxes=[]; self.all_labels=[]; self._neutral_btns=[]; self._text_widgets=[]
        self._title_labels=[]; self._btn_labels=[]; self._info_labels=[]

        # ── 顶部栏 ──
        top = ctk.CTkFrame(self.root,fg_color="transparent")
        top.pack(fill=tk.X,padx=18,pady=(12,6))
        if self._ico_img is not None:
            logo = ctk.CTkLabel(top,image=self._ico_img,text="",width=26,height=26)
            logo.pack(side=tk.LEFT,padx=(0,8))
        lbl = ctk.CTkLabel(top,text=t('title'),font=FONT_T,text_color=c["fg"]); lbl.pack(side=tk.LEFT)
        self.all_labels.append(lbl)

        # 语言切换（主题左边）+ 主题切换
        self.btn_lang = ctk.CTkButton(top,text=t('btn_lang'),font=FONT,
            fg_color=c["border"],hover_color=c["fg2"],text_color=c["fg"],
            corner_radius=6,height=28,width=40,command=self._toggle_lang)
        self.btn_lang.pack(side=tk.RIGHT,padx=(4,0)); self._neutral_btns.append(self.btn_lang)
        self._btn_labels.append((self.btn_lang,'btn_lang'))

        self.btn_theme = ctk.CTkButton(top,text=t('btn_theme_light'),font=FONT,
            fg_color=c["border"],hover_color=c["fg2"],text_color=c["fg"],
            corner_radius=6,height=28,width=80,command=self._toggle_theme)
        self.btn_theme.pack(side=tk.RIGHT); self._neutral_btns.append(self.btn_theme)

        # ── 主体 ──
        body = ctk.CTkFrame(self.root,fg_color="transparent")
        body.pack(fill=tk.BOTH,expand=True,padx=18,pady=(0,6))
        body.grid_columnconfigure(0,weight=2); body.grid_columnconfigure(1,weight=3)
        body.grid_rowconfigure(0,weight=1)
        left = ctk.CTkFrame(body,fg_color="transparent"); left.grid(row=0,column=0,sticky="nsew",padx=(0,6))
        right = ctk.CTkFrame(body,fg_color="transparent"); right.grid(row=0,column=1,sticky="nsew",padx=(6,0))
        right.grid_columnconfigure(0,weight=1); right.grid_rowconfigure(0,weight=0); right.grid_rowconfigure(1,weight=1)

        # ── ① 文件选择 ──
        fc = self._card(left); fc.pack(fill=tk.X,pady=(0,6))
        lbl = ctk.CTkLabel(fc,text=t('select_file'),font=FONT_B,text_color=c["fg2"])
        lbl.pack(anchor="w",padx=11,pady=(10,4)); self.all_labels.append(lbl)
        self._title_labels.append((lbl,'select_file'))
        br = ctk.CTkFrame(fc,fg_color="transparent"); br.pack(fill=tk.X,padx=11,pady=(0,4))
        self.btn_sel = ctk.CTkButton(br,text=t('btn_select'),font=FONT,
            fg_color=c["border"],hover_color=c["border"],text_color="#fff",
            corner_radius=6,height=32,width=110,command=self._select)
        self.btn_sel.pack(side=tk.LEFT,padx=(0,5)); self._neutral_btns.append(self.btn_sel)
        self._btn_labels.append((self.btn_sel,'btn_select'))
        btn_batch = ctk.CTkButton(br,text=t('btn_batch'),font=FONT,
            fg_color=c["border"],hover_color=c["fg2"],text_color=c["fg"],
            corner_radius=6,height=32,width=90,command=self._batch)
        btn_batch.pack(side=tk.LEFT,padx=(0,5)); self._neutral_btns.append(btn_batch)
        self._btn_labels.append((btn_batch,'btn_batch'))
        ctk.CTkButton(br,text=t('btn_clear'),font=FONT,fg_color=c["danger"],
            hover_color=c["danger"],text_color="#fff",corner_radius=6,
            height=32,width=70,command=self._clear).pack(side=tk.LEFT)
        fl_frame = ctk.CTkFrame(fc,fg_color="transparent",corner_radius=0)
        fl_frame.pack(fill=tk.X,padx=11,pady=(4,10))
        fl_frame.grid_columnconfigure(0,weight=1); fl_frame.grid_rowconfigure(0,weight=1)
        self.file_list = tk.Text(fl_frame,font=FONT_S,bg=c["input"],fg=c["fg"],
            relief="flat",borderwidth=0,height=5,state="disabled",wrap="none",undo=False)
        self.file_list.grid(row=0,column=0,sticky="nsew")
        fl_sb = ctk.CTkScrollbar(fl_frame,orientation="vertical",height=105,command=self.file_list.yview)
        fl_sb.grid(row=0,column=1,sticky="ns")
        self.file_list.configure(yscrollcommand=fl_sb.set)
        self._text_widgets.append(self.file_list)

        # ── ② 文件信息 ──
        ic = self._card(left); ic.pack(fill=tk.X,pady=(0,6))
        lbl = ctk.CTkLabel(ic,text=t('file_info'),font=FONT_B,text_color=c["fg2"])
        lbl.pack(anchor="w",padx=11,pady=(10,4)); self.all_labels.append(lbl)
        self._title_labels.append((lbl,'file_info'))
        self.info_frame = ctk.CTkFrame(ic,fg_color=c["input"],corner_radius=6)
        self.info_frame.pack(fill=tk.X,padx=11,pady=(2,10))
        self.boxes.append(self.info_frame); self.info_lbls={}
        for key in ('fn','fmt','codec_l','br','sr','ch','dur'):
            row = ctk.CTkFrame(self.info_frame,fg_color="transparent")
            row.pack(fill=tk.X,padx=8,pady=1)
            lbl = ctk.CTkLabel(row,text=f"{t(key)}：",font=FONT_S,text_color=c["fg2"],width=60,anchor="w")
            lbl.pack(side=tk.LEFT); self._info_labels.append((lbl,key))
            v = ctk.CTkLabel(row,text="—",font=FONT_S,text_color=c["fg"],anchor="w")
            v.pack(side=tk.LEFT,padx=(3,0)); self.info_lbls[key]=v

        # ── ③ 输出设置 ──
        oc = self._card(left); oc.pack(fill=tk.X)
        lbl = ctk.CTkLabel(oc,text=t('output'),font=FONT_B,text_color=c["fg2"])
        lbl.pack(anchor="w",padx=11,pady=(10,4)); self.all_labels.append(lbl)
        self._title_labels.append((lbl,'output'))
        sr = ctk.CTkFrame(oc,fg_color="transparent"); sr.pack(fill=tk.X,padx=11,pady=2)
        self.same_sw = ctk.CTkSwitch(sr,text=t('same_dir'),font=FONT_S,
            text_color=c["fg"],progress_color=c["accent"],button_color=c["accent"],command=self._tog_dir)
        self.same_sw.pack(side=tk.LEFT); self.same_sw.select()
        dr = ctk.CTkFrame(oc,fg_color="transparent"); dr.pack(fill=tk.X,padx=11,pady=(4,2))
        self.out_entry = ctk.CTkEntry(dr,font=FONT_S,fg_color=c["input"],text_color=c["fg"],
            corner_radius=6,border_width=1,border_color=c["border"],state="disabled")
        self.out_entry.pack(side=tk.LEFT,fill=tk.X,expand=True,padx=(0,5))
        self.btn_browse = ctk.CTkButton(dr,text=t('btn_browse'),font=FONT,
            fg_color=c["border"],hover_color=c["fg2"],text_color=c["fg"],
            corner_radius=6,height=28,width=65,state="disabled",command=self._browse)
        self.btn_browse.pack(side=tk.RIGHT); self._neutral_btns.append(self.btn_browse)
        self._btn_labels.append((self.btn_browse,'btn_browse'))

        # ── ④ 进度 ──
        pc = self._card(right); pc.grid(row=0,column=0,sticky="ew",pady=(0,6))
        lbl = ctk.CTkLabel(pc,text=t('progress'),font=FONT_B,text_color=c["fg2"])
        lbl.pack(anchor="w",padx=11,pady=(10,4)); self.all_labels.append(lbl)
        self._title_labels.append((lbl,'progress'))
        self.pbar = ctk.CTkProgressBar(pc,mode="determinate",height=8,corner_radius=4,
            progress_color=c["accent"],fg_color=c["border"])
        self.pbar.pack(fill=tk.X,padx=11,pady=(2,5)); self.pbar.set(0)
        self.status_lbl = ctk.CTkLabel(pc,text=t('ready'),font=FONT_S,text_color=c["fg2"],anchor="w")
        self.status_lbl.pack(anchor="w",padx=11,pady=(0,10))

        # ── ⑤ 日志 ──
        lc = self._card(right); lc.grid(row=1,column=0,sticky="nsew")
        lc.grid_columnconfigure(0,weight=1); lc.grid_rowconfigure(0,weight=0); lc.grid_rowconfigure(1,weight=1)
        lh = ctk.CTkFrame(lc,fg_color="transparent")
        lh.grid(row=0,column=0,sticky="ew",padx=11,pady=(10,4))
        lbl = ctk.CTkLabel(lh,text=t('log'),font=FONT_B,text_color=c["fg2"])
        lbl.pack(side=tk.LEFT); self.all_labels.append(lbl)
        self._title_labels.append((lbl,'log'))
        btn_clog = ctk.CTkButton(lh,text=t('btn_clear_log'),font=FONT,
            fg_color=c["border"],hover_color=c["fg2"],text_color=c["fg"],
            corner_radius=4,height=22,width=45,command=self._clear_log)
        btn_clog.pack(side=tk.RIGHT); self._neutral_btns.append(btn_clog)
        self._btn_labels.append((btn_clog,'btn_clear_log'))
        log_frame = ctk.CTkFrame(lc,fg_color="transparent",corner_radius=0)
        log_frame.grid(row=1,column=0,sticky="nsew",padx=11,pady=(2,10))
        log_frame.grid_columnconfigure(0,weight=1); log_frame.grid_rowconfigure(0,weight=1)
        self.log = tk.Text(log_frame,font=MONO,bg=c["input"],fg=c["fg"],
            relief="flat",borderwidth=0,state="disabled",wrap="word",undo=False)
        self.log.grid(row=0,column=0,sticky="nsew")
        log_sb = ctk.CTkScrollbar(log_frame,orientation="vertical",command=self.log.yview)
        log_sb.grid(row=0,column=1,sticky="ns")
        self.log.configure(yscrollcommand=log_sb.set)
        self._text_widgets.append(self.log)

        # ── 底栏 ──
        bar = ctk.CTkFrame(self.root,fg_color="transparent")
        bar.pack(fill=tk.X,padx=18,pady=(0,12))
        btn_open = ctk.CTkButton(bar,text=t('btn_open_dir'),font=FONT,
            fg_color=c["border"],hover_color=c["fg2"],text_color=c["fg"],
            corner_radius=6,height=36,width=140,command=self._open_dir)
        btn_open.pack(side=tk.LEFT); self._neutral_btns.append(btn_open)
        self._btn_labels.append((btn_open,'btn_open_dir'))
        self.btn_cancel = ctk.CTkButton(bar,text=t('btn_cancel'),font=FONT,
            fg_color=c["danger"],hover_color=c["danger"],text_color="#fff",
            corner_radius=6,height=36,width=80,state="disabled",command=self._cancel)
        self.btn_cancel.pack(side=tk.RIGHT,padx=(6,0))
        self.btn_run = ctk.CTkButton(bar,text=t('btn_start'),font=FONT,
            fg_color=c["border"],hover_color=c["border"],text_color="#fff",
            corner_radius=6,height=36,width=140,command=self._start)
        self.btn_run.pack(side=tk.RIGHT); self._neutral_btns.append(self.btn_run)
        self._btn_labels.append((self.btn_run,'btn_start'))
        self.btn_swap = ctk.CTkButton(bar,text=t('btn_swap'),font=FONT,
            fg_color=c["border"],hover_color=c["border"],text_color="#fff",
            corner_radius=6,height=36,width=140,command=self._start_swap)
        self.btn_swap.pack(side=tk.RIGHT,padx=(0,6)); self._neutral_btns.append(self.btn_swap)
        self._btn_labels.append((self.btn_swap,'btn_swap'))

    def _card(self,parent):
        c = ctk.CTkFrame(parent,fg_color=self.c["surface"],corner_radius=10,
            border_width=1,border_color=self.c["border"])
        self.cards.append(c); return c

    def _center(self):
        self.root.update_idletasks()
        sw,sh = self.root.winfo_screenwidth(),self.root.winfo_screenheight()
        self.root.geometry(f"+{(sw-W)//2}+{(sh-H)//2}")

    # ═══════════════════════════════════════════════════
    # 文件
    # ═══════════════════════════════════════════════════

    def _add(self,fp):
        if any(f['filepath']==fp for f in self.files): return
        info = probe(fp)
        t = self._t
        if not info: return messagebox.showwarning(t('dlog_read'),f"{t('dlog_cant_read')}{os.path.basename(fp)}")
        if info['channels']<2:
            return messagebox.showwarning(t('dlog_non_stereo'),
                t('dlog_channels',info['channels'])+os.path.basename(fp))
        self.files.append(info); self._refresh()

    def _select(self):
        t = self._t
        fp = filedialog.askopenfilename(title=t('dlog_pick_file'),
            filetypes=[(t('media_filter'),"*"+";*".join(MEDIA_EXTS)),(t('all_files'),"*.*")])
        if fp: self._add(fp)

    def _batch(self):
        t = self._t
        for fp in filedialog.askopenfilenames(title=t('dlog_pick_batch'),
            filetypes=[(t('media_filter'),"*"+";*".join(MEDIA_EXTS)),(t('all_files'),"*.*")]):
            self._add(fp)

    def _clear(self): self.files.clear(); self._refresh()

    def _refresh(self):
        t = self._t
        self.file_list.configure(state="normal"); self.file_list.delete("1.0",tk.END)
        if not self.files: self.file_list.insert(tk.END,t('no_files'))
        else:
            for i,x in enumerate(self.files):
                self.file_list.insert(tk.END,
                    f"  [{i+1}] {x['filename']}  |  {x['format']}  "
                    f"|  {x['channels']}ch  |  {fmt_br(x['bit_rate'])}  |  {fmt_dur(x['duration'])}\n")
        self.file_list.configure(state="disabled")
        if not self.files:
            for v in self.info_lbls.values(): v.configure(text="—")
        else:
            x = self.files[0]
            self.info_lbls['fn'].configure(text=x['filename'])
            self.info_lbls['fmt'].configure(text=x['format'])
            self.info_lbls['codec_l'].configure(text=f"{x['codec']} ({x['codec_long']})")
            self.info_lbls['br'].configure(text=fmt_br(x['bit_rate']) if x['bit_rate']>0 else '(VBR)')
            self.info_lbls['sr'].configure(text=f"{x['sample_rate']} Hz" if x['sample_rate']>0 else '—')
            self.info_lbls['ch'].configure(text=f"{x['channels']} ({x['channel_layout']})")
            self.info_lbls['dur'].configure(text=fmt_dur(x['duration']))

    # ═══════════════════════════════════════════════════
    # 输出
    # ═══════════════════════════════════════════════════

    def _tog_dir(self):
        self.same_dir = self.same_sw.get()
        s = "disabled" if self.same_dir else "normal"
        self.out_entry.configure(state=s); self.btn_browse.configure(state=s); self._refresh()

    def _browse(self):
        d = filedialog.askdirectory(title=self._t('dlog_pick_dir'))
        if d: self.custom_dir = d; self.out_entry.delete(0,tk.END); self.out_entry.insert(0,d)

    def _out(self,info):
        return os.path.dirname(info['filepath']) if self.same_dir else (self.custom_dir or os.path.dirname(info['filepath']))

    # ═══════════════════════════════════════════════════
    # 处理
    # ═══════════════════════════════════════════════════

    def _start(self): self._begin('split')
    def _start_swap(self): self._begin('swap')

    def _begin(self, mode):
        t = self._t
        if not self.files: return messagebox.showinfo(t('dlog_info'),t('dlog_info_add'))
        if self.running: return
        if not self.same_dir and (not self.custom_dir or not os.path.isdir(self.custom_dir)):
            return messagebox.showwarning(t('dlog_warn'),t('dlog_warn_msg'))
        conflicts = []
        for info in self.files:
            if mode=='swap':
                _,out = build_swap_cmd(info,self._out(info)); outs=[out]
            else:
                _,lp,rp = build_cmd(info,self._out(info)); outs=[lp,rp]
            for p in outs:
                if os.path.exists(p): conflicts.append(os.path.basename(p))
        if conflicts:
            if not messagebox.askyesno(t('dlog_overwrite'),
                t('dlog_overwrite_msg',len(conflicts))+
                "\n".join(f"  • {c}" for c in conflicts[:6])+
                (t('dlog_overwrite_more',len(conflicts)-6) if len(conflicts)>6 else "")+
                t('dlog_overwrite_ask')): return
        self.mode = mode
        self.running=True; self.cancelled=False; c=self.c
        self.btn_run.configure(state="disabled",text=t('processing'),fg_color=c["border"],hover_color=c["border"])
        self.btn_swap.configure(state="disabled")
        self.btn_cancel.configure(state="normal"); self.btn_sel.configure(state="disabled")
        self.pbar.set(0); self.status_lbl.configure(text=t('preparing'))
        threading.Thread(target=self._worker,daemon=True).start()

    def _cancel(self):
        if not self.running: return
        self.cancelled=True; self._log(self._t('cancelling'))
        if self.proc:
            try: self.proc.kill()
            except: pass; self.proc=None

    def _worker(self):
        t = self._t; total,ok,fail = len(self.files),0,0; failed=[]
        for idx,info in enumerate(self.files):
            if self.cancelled: break
            seq,od = idx+1,self._out(info)
            if self.mode=='swap':
                cmd,out = build_swap_cmd(info,od); outs=[out]
                self._log(f"[{seq}/{total}] {info['filename']}")
                self._log(f"  ↔ -> {os.path.basename(out)}")
            else:
                cmd,lp,rp = build_cmd(info,od); outs=[lp,rp]
                self._log(f"[{seq}/{total}] {info['filename']}")
                self._log(f"  L -> {os.path.basename(lp)}"); self._log(f"  R -> {os.path.basename(rp)}")
            os.makedirs(od,exist_ok=True); dur_us = info['duration']*1_000_000
            try:
                si = subprocess.STARTUPINFO(); si.dwFlags|=subprocess.STARTF_USESHOWWINDOW
                p = subprocess.Popen(cmd,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,startupinfo=si)
                self.proc = p
                for raw in p.stderr:
                    if self.cancelled: p.kill(); break
                    line = raw.decode('utf-8',errors='replace'); ls = line.strip()
                    if not ls: continue
                    if ls.startswith('out_time_ms=') and dur_us>0:
                        try:
                            cur = int(ls.split('=',1)[1]); v = min(cur/dur_us,0.99)
                            self.root.after(0,lambda v=v,i=idx,t=total:self.pbar.set((i+v)/t))
                            self.root.after(0,lambda n=info['filename'],s=seq,t=total,v=v:
                                self.status_lbl.configure(text=f"[{s}/{t}] {n}  ({v*100:.0f}%)"))
                        except: pass
                    elif not ls.startswith(('frame=','fps=','q=','size=','bitrate=','speed=')):
                        self._log(f"    {ls}")
                p.wait(); rc = p.returncode; self.proc=None
                if self.cancelled:
                    for pth in outs:
                        try:
                            if os.path.exists(pth): os.remove(pth)
                        except: pass
                    self._log(t('cancelled_clean')); break
                if rc==0: ok+=1; self._log(t('done_ok'))
                else: fail+=1; failed.append(info['filename']); self._log(t('done_fail',rc))
            except Exception as ex:
                fail+=1; failed.append(info['filename']); self.proc=None; self._log(t('done_err',ex))
            self.root.after(0,lambda v=(idx+1)/total:self.pbar.set(v))
        self.running=False; self.proc=None; c=self.c
        self.root.after(0,lambda: self.btn_run.configure(
            state="normal",text=t('btn_start'),fg_color=c["accent"],hover_color=c["accent"]))
        self.root.after(0,lambda: self.btn_swap.configure(state="normal"))
        self.root.after(0,lambda: self.btn_cancel.configure(state="disabled"))
        self.root.after(0,lambda: self.btn_sel.configure(state="normal"))
        if self.cancelled:
            final = t('status_cancelled',ok,fail); sum_tag = t('summary_cancelled')
        else:
            final = t('status_done',ok,fail); sum_tag = t('summary_done')
        self.root.after(0,lambda f=final:self.status_lbl.configure(text=f))
        self._log("="*40); self._log(t('summary',sum_tag,ok,fail))
        for fn in failed: self._log(t('failed_file',fn))

    # ═══════════════════════════════════════════════════
    # 日志 & 工具
    # ═══════════════════════════════════════════════════

    def _log(self,msg):
        ts = time.strftime('%H:%M:%S')
        self.root.after(0,lambda: self._write(f"[{ts}] {msg}"))

    def _write(self,line):
        self.log.configure(state="normal"); self.log.insert(tk.END,line+"\n")
        self.log.see(tk.END); self.log.configure(state="disabled")

    def _clear_log(self):
        self.log.configure(state="normal"); self.log.delete("1.0",tk.END); self.log.configure(state="disabled")

    def _open_dir(self):
        t = self._t
        d = self._out(self.files[0]) if self.files else (self.custom_dir or "")
        os.startfile(d) if d and os.path.isdir(d) else messagebox.showinfo(t('dlog_info'),t('dir_not_exist'))

    def _close(self):
        t = self._t
        if self.running:
            if messagebox.askyesno(t('dlog_close'),t('dlog_close_ask')):
                self.cancelled=True
                if self.proc:
                    try: self.proc.kill()
                    except: pass
                self.root.destroy()
        else: self.root.destroy()

if __name__=='__main__':
    try:
        subprocess.run(['ffmpeg','-version'],capture_output=True,timeout=5,check=True,creationflags=CREATE_NO_WINDOW)
        subprocess.run(['ffprobe','-version'],capture_output=True,timeout=5,check=True,creationflags=CREATE_NO_WINDOW)
    except Exception:
        messagebox.showerror("Missing Dependency",T['zh']['missing_ffmpeg'])
        sys.exit(1)
    App()
