#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
=============================================================================
CALLBACK HANDLERS
=============================================================================
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from utils.logger import logger
from utils.exceptions import handle_errors
from database.models import Constants


# ===== AGREE 18 CALLBACK =====

@handle_errors
async def agree_18_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User menyetujui disclaimer"""
    query = update.callback_query
    await query.answer()
    
    # Daftar role
    roles = [
        ('ipar', 'Ipar'),
        ('teman_kantor', 'Teman Kantor'),
        ('janda', 'Janda'),
        ('pelakor', 'Pelakor'),
        ('istri_orang', 'Istri Orang'),
        ('pdkt', 'PDKT'),
        ('sepupu', 'Sepupu'),
        ('teman_sma', 'Teman SMA'),
        ('mantan', 'Mantan')
    ]
    
    # Buat keyboard 2 kolom
    keyboard = []
    for i in range(0, len(roles), 2):
        row = []
        row.append(InlineKeyboardButton(roles[i][1], callback_data=f"role_{roles[i][0]}"))
        if i+1 < len(roles):
            row.append(InlineKeyboardButton(roles[i+1][1], callback_data=f"role_{roles[i+1][0]}"))
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✨ **Pilih Role**\n\n"
        "• Ipar\n• Teman Kantor\n• Janda\n• Pelakor\n"
        "• Istri Orang\n• PDKT\n• Sepupu\n• Teman SMA\n• Mantan",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )
    
    return Constants.SELECTING_ROLE


# ===== ROLE CALLBACK =====

@handle_errors
async def role_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User memilih role"""
    query = update.callback_query
    await query.answer()
    
    role = query.data.replace("role_", "")
    
    await query.edit_message_text(
        f"✅ Role **{role}** dipilih.\n\n"
        f"Fitur sedang dalam pengembangan.",
        parse_mode='Markdown'
    )
    
    return Constants.ACTIVE_SESSION


# ===== START PAUSE CALLBACK =====

@handle_errors
async def start_pause_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback untuk unpause atau new"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "unpause":
        await query.edit_message_text("▶️ Sesi dilanjutkan!")
        return Constants.ACTIVE_SESSION
    else:
        return await agree_18_callback(update, context)


# ===== CLOSE CALLBACK =====

@handle_errors
async def close_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback untuk close"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "close_no":
        await query.edit_message_text("💕 Lanjutkan...")
        return ConversationHandler.END
    
    await query.edit_message_text("🔒 Sesi ditutup. Terima kasih!")
    return ConversationHandler.END


# ===== END CALLBACK =====

@handle_errors
async def end_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Callback untuk end"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "end_no":
        await query.edit_message_text("💕 Lanjutkan...")
        return ConversationHandler.END
    
    await query.edit_message_text("💔 Hubungan berakhir. Sampai jumpa!")
    return ConversationHandler.END


# ===== RELATIONSHIP CALLBACKS =====

@handle_errors
async def jadipacar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "jadipacar_no":
        await query.edit_message_text("💕 Baiklah...")
        return ConversationHandler.END
    
    await query.edit_message_text("💕 Kita pacaran sekarang!")
    return ConversationHandler.END


@handle_errors
async def break_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "break_no":
        await query.edit_message_text("💕 Lanjutkan...")
        return ConversationHandler.END
    
    await query.edit_message_text("⏸️ Kita break dulu...")
    return ConversationHandler.END


@handle_errors
async def breakup_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "breakup_no":
        await query.edit_message_text("💕 Lanjutkan...")
        return ConversationHandler.END
    
    await query.edit_message_text("💔 Putus... kita jadi FWB")
    return ConversationHandler.END


@handle_errors
async def fwb_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "fwb_no":
        await query.edit_message_text("💕 Baiklah...")
        return ConversationHandler.END
    
    await query.edit_message_text("🔥 Sekarang kita FWB!")
    return ConversationHandler.END


# ===== ROLE-SPECIFIC CALLBACKS =====

async def role_ipar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_teman_kantor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_janda_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_pelakor_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_istri_orang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_pdkt_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_sepupu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_teman_sma_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)

async def role_mantan_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    return await role_callback(update, context)
