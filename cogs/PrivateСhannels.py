import disnake
from disnake.ext import commands

texts = {
    "🏷": {"start": "Введите новое название комнаты", "end": ""},
    "👥": {"start": "Введите новое количество пользователей", "end": ""},
    "🔒": {"start": "Вы успешно закрыли комнату", "end": ""},
    "🔓": {"start": "Вы успешно открыли комнату", "end": ""},
    "🚪": {"start": "Упомяните пользователя, которого желаете выгнать с комнаты", "end": ""},
    "✔": {"start": "Упомяните пользователя, которому желаете дать доступ к комнате", "end": ""},
    "❌": {"start": "Упомяните пользователя, у которого желаете забрать доступ к комнате", "end": ""},
    "👑": {"start": "Упомяните пользователя, которому желаете передать владение комнатой", "end": ""}
}


class Buttons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=0)

    @disnake.ui.button(label="", emoji="🏷")
    async def _pan(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="👥")
    async def _users(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="🔒")
    async def _lock(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="🔓")
    async def _unlock(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="🚪", row=2)
    async def _dver(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="✔", row=2)
    async def _dat(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="❌", row=2)
    async def _nedat(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass

    @disnake.ui.button(label="", emoji="👑", row=2)
    async def _korona(self, button: disnake.ui.button, interaction: disnake.MessageInteraction):
        pass


class PrivateRooms(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voices = {}
        self.msg_id = int

    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(1059440775512981574)
        await channel.purge()
        embed = disnake.Embed(
            title="Управление вашей приватной комнатой",
            colour=disnake.Colour.green()
        )
        embed.description = """\n
            🏷️ - Изменить название комнаты
            👥 - Изменить кол-во слотов
            🔒 - Закрыть комнату для всех
            🔓 - Открыть комнату для всех
            🚪 - Выгнать пользователя с комнаты
            ✔ - Дать доступ пользователю в комнату
            ❌ - Забрать доступ пользователю в комнату
            👑 - Передать владение комнатой
        """
        msg = await channel.send(embed=embed, view=Buttons())
        self.msg_id = msg.id

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel and after.channel.id == 777968491385978902:
            channel = await member.guild.create_voice_channel(
                name=member.display_name,
                category=after.channel.category
            )
            await member.move_to(channel=channel)
            self.voices[channel.id] = member.id
        if before.channel and before.channel.id in self.voices and not len(before.channel.members):
            await before.channel.delete()
            del self.voices[before.channel.id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 1059440775512981574 and message.author.id != self.bot.user.id:
            await message.delete()

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        if interaction.message.id != self.msg_id:
            return
        if not interaction.author.voice:
            return await interaction.response.send_message(
                "Похоже вы не в Голосовом канале..",
                ephemeral=True
            )
        member = interaction.guild.get_member(interaction.author.id)
        channel = member.voice.channel
        if member.id == self.voices[channel.id]:
            await interaction.response.send_message(texts[interaction.component.emoji.name]["start"], ephemeral=True)
            if interaction.component.emoji.name == "🏷":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                await channel.edit(name=msg.content)
            elif interaction.component.emoji.name == "👥":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if msg.content.isdigit():
                    await channel.edit(user_limit=int(msg.content))
            elif interaction.component.emoji.name == "🔒":
                await channel.set_permissions(
                    interaction.guild.default_role,
                    connect=False
                )
            elif interaction.component.emoji.name == "🔓":
                await channel.set_permissions(
                    interaction.guild.default_role,
                    connect=True
                )
            elif interaction.component.emoji.name == "🚪":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        if u.voice.channel == channel:
                            await u.move_to(channel=None)
            elif interaction.component.emoji.name == "✔":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        await channel.set_permissions(
                            u,
                            connect=True
                        )
            elif interaction.component.emoji.name == "❌":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    for u in msg.mentions:
                        await channel.set_permissions(
                            u,
                            connect=False
                        )
            elif interaction.component.emoji.name == "👑":
                msg = await self.bot.wait_for("message", check=lambda x: x.author == interaction.author, timeout=15)
                if len(msg.mentions):
                    self.voices[channel.id] = msg.mentions[0].id
            else:
                return await interaction.followup.send(texts[interaction.component.emoji.name]["end"], ephemeral=True)
        else:
            return await interaction.response.send_message(
                "Прости, похоже, что ты не можешь настраивать этот канал :(",
                ephemeral=True
            )

def setup(bot):
    bot.add_cog(PrivateRooms(bot))
