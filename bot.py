import discord
‏from discord.ext import commands
‏from discord.ui import Select, View

# إعداد البوت مع الصلاحيات المطلوبة
‏intents = discord.Intents.default()
‏intents.members = True
‏intents.message_content = True

‏bot = commands.Bot(command_prefix="!", intents=intents)

‏@bot.event
‏async def on_ready():
‏    print(f"تم تسجيل الدخول بنجاح باسم: {bot.user.name}")

# ==================== 1. أمر التايم أوت مع قائمة الأسباب (!time) ====================
‏class TimeoutSelect(Select):
‏    def __init__(self, member: discord.Member):
‏        self.target_member = member
‏        options = [
‏            discord.SelectOption(label="🤬 سب", description="المدة: 10 دقائق", value="spam_bad"),
‏            discord.SelectOption(label="🔁 سبام", description="المدة: دقيقة واحدة", value="spam_msg"),
‏            discord.SelectOption(label="📢 إعلان بدون إذن", description="المدة: 5 دقائق", value="ad_no"),
‏            discord.SelectOption(label="⚠️ مخالفة قوانين", description="المدة: 5 دقائق", value="rule_break"),
        ]
‏        super().__init__(placeholder="اختر سبب التايم أوت...", min_values=1, max_values=1, options=options)

‏    async def callback(self, interaction: discord.Interaction):
‏        import datetime
        
‏        if self.values[0] == "spam_bad":
‏            duration = discord.utils.utcnow() + datetime.timedelta(minutes=10)
‏            reason = "سب"
‏        elif self.values[0] == "spam_msg":
‏            duration = discord.utils.utcnow() + datetime.timedelta(minutes=1)
‏            reason = "سبام"
‏        elif self.values[0] == "ad_no":
‏            duration = discord.utils.utcnow() + datetime.timedelta(minutes=5)
‏            reason = "إعلان بدون إذن"
‏        elif self.values[0] == "rule_break":
‏            duration = discord.utils.utcnow() + datetime.timedelta(minutes=5)
‏            reason = "مخالفة قوانين"

‏        try:
‏            await self.target_member.timeout(duration, reason=reason)
‏            await interaction.response.send_message(f"✅ تم إعطاء تايم أوت لـ {self.target_member.mention} بنجاح.\n📝 السبب: **{reason}**", ephemeral=False)
‏        except Exception as e:
‏            await interaction.response.send_message(f"❌ حدث خطأ أثناء تنفيذ التايم أوت: {e}", ephemeral=True)

‏class TimeoutView(View):
‏    def __init__(self, member: discord.Member):
‏        super().__init__()
‏        self.add_item(TimeoutSelect(member))

‏@bot.command()
‏@commands.has_permissions(moderate_members=True)
‏async def time(ctx, member: discord.Member):
‏    view = TimeoutView(member)
‏    await ctx.send(f"اختر سبب التايم أوت للعضو {member.mention}:", view=view)

# ==================== 2. أمر الباند المباشر (!ban) ====================
‏@bot.command()
‏@commands.has_permissions(ban_members=True)
‏async def ban(ctx, member: discord.Member, *, reason=None):
‏    await member.ban(reason=reason)
‏    await ctx.send(f"🔨 تم حظر العضو {member.mention} بنجاح.")

# ==================== 3. أمر الكيك المباشر (!kick) ====================
‏@bot.command()
‏@commands.has_permissions(kick_members=True)
‏async def kick(ctx, member: discord.Member, *, reason=None):
‏    await member.kick(reason=reason)
‏    await ctx.send(f"👢 تم طرد العضو {member.mention} بنجاح.")

# ==================== 4. أمر تغيير الاسم (!nick) ====================
‏@bot.command()
‏@commands.has_permissions(manage_nicknames=True)
‏async def nick(ctx, member: discord.Member, *, new_name: str):
‏    try:
‏        await member.edit(nick=new_name)
‏        await ctx.send(f"✏️ تم تغيير اسم {member.mention} إلى **{new_name}** بنجاح.")
‏    except Exception as e:
‏        await ctx.send(f"❌ لم أستطيع تغيير الاسم، تأكد من أن رتبة البوت أعلى من العضو. الخطأ: {e}")

# ==================== 5. أمر إعطاء رول (!role) ====================
‏@bot.command()
‏@commands.has_permissions(manage_roles=True)
‏async def role(ctx, member: discord.Member, *, role_name: str):
‏    found_role = discord.utils.get(ctx.guild.roles, name=role_name)
    
‏    if not found_role:
‏        await ctx.send(f"❌ لم يتم العثور على رول بهذا الاسم: `{role_name}`")
‏        return

‏    try:
‏        await member.add_roles(found_role)
‏        await ctx.send(f"✅ تم إعطاء الرول **{found_role.name}** للعضو {member.mention} بنجاح.")
‏    except Exception as e:
‏        await ctx.send(f"❌ حدث خطأ (تأكد أن رتبة البوت أعلى من الرول المطلوب): {e}")

# ==================== 6. أمر كتابة قوانين السيرفر (!rules) ====================
‏@bot.command()
‏@commands.has_permissions(administrator=True)
‏async def rules(ctx):
‏    try:
‏        await ctx.message.delete()
‏    except:
‏        pass
    
‏    embed = discord.Embed(
‏        title="📜 قوانين سيرفر ديسكورد الرسمي",
‏        description="يرجى الالتزام بالقوانين التالية تجنباً للعقوبات الإدارية:",
‏        color=discord.Color.blue()
    )
‏    embed.add_field(name="1️⃣ احترام الجميع", value="يُمنع التبادل بالشتائم أو الإهانة نهائياً.", inline=False)
‏    embed.add_field(name="2️⃣ ممنوع السبام", value="يُحظر تكرار الرسائل أو الحروف بشكل مزعج.", inline=False)
‏    embed.add_field(name="3️⃣ الإعلانات", value="يُمنع نشر روابط سيرفرات أو إعلانات بدون إذن الإدارة.", inline=False)
‏    embed.add_field(name="4️⃣ المواضيع الحساسة", value="يُمنع منعاً باتاً التطرق للمواضيع السياسية أو الطائفية.", inline=False)
‏    embed.set_footer(text="الإدارة تحظى بالحق الكامل لمعاقبة أي مخالف.")
    
‏    await ctx.send(embed=embed)

bot.run("MTU2OTczNzM5ODIxMDc5MzUxMg.GR9TL3.guqs-m1L2__bQhzAG5XEJUAB0wIBPydyVOLfI4")
