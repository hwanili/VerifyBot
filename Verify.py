import nextcord
import asyncio
from nextcord.ext import commands
from nextcord.ui import Button, View, Modal, TextInput

intents = nextcord.Intents.default()
intents.message_content = True

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = #관리자 아이디
TOKEN = " " #봇토큰

@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user}')

def is_admin(user):
    return user.id == admin_id

@bot.slash_command(name="인증", description="아래 버튼을 눌러 역할을 지급합니다.")
async def btrole(interaction: nextcord.Interaction):
    if not is_admin(interaction.user):
        embed = nextcord.Embed(
            title="권한 없음",
            description="이 명령어는 관리자만 사용할 수 있습니다.",
            color=nextcord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    embed = nextcord.Embed(title="인증하기", description="아래 버튼을 누르면 역할이 지급됩니다", color=nextcord.Color.green())
    await interaction.response.send_message(embed=embed, view=RoleButton(interaction))

class RoleButton(nextcord.ui.View):
    def __init__(self, interaction):
        super().__init__(timeout=None)
        self.interaction = interaction

    @nextcord.ui.button(label="인증하기", style=nextcord.ButtonStyle.green, custom_id="verification_button")
    async def charge(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        member = interaction.guild.get_member(interaction.user.id)
        role = nextcord.utils.get(interaction.guild.roles, name=" ") #name=" "안에 인증 아이디 적으세요
        if role:
            await member.add_roles(role)
            await interaction.response.send_message("인증이 완료되었습니다.", ephemeral=True)
        else:
            await interaction.response.send_message("역할을 찾을 수 없습니다. 관리자에게 문의하세요.", ephemeral=True)

bot.run(TOKEN)
