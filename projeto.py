import random
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt

# Inicializa o console do Rich
console = Console()

# ==========================================
# 1. A LÓGICA DO PERSONAGEM (POO)
# ==========================================
class Personagem:
    def __init__(self, nome, raca, classe):
        self.nome = nome
        self.raca = raca
        self.classe = classe
        self.nivel = 1
        self.vida_max = 100
        self.mana_max = 50
        self.ataque_base = 10
        
        # Aplicando as vantagens de cada Raça
        if raca == "Humano":
            self.ataque_base += 2
        elif raca == "Elfo":
            self.mana_max += 25  
        elif raca == "Anão":
            self.vida_max += 30  
        elif raca == "Orc":
            self.ataque_base += 7  
        elif raca == "Draconato":
            self.vida_max += 15
            self.mana_max += 10

        self.vida = self.vida_max
        self.mana = self.mana_max
        self.golpes = self.definir_golpes_da_classe()

    def definir_golpes_da_classe(self):
        if self.classe == "Mago":
            return [
                {"nome": "Bola de Fogo", "dano": 25, "custo_mana": 15},
                {"nome": "Relâmpago", "dano": 35, "custo_mana": 25},
                {"nome": "Dreno de Mana", "dano": 10, "custo_mana": 0} 
            ]
        elif self.classe == "Guerreiro":
            return [
                {"nome": "Golpe Devastador", "dano": 20, "custo_mana": 5},
                {"nome": "Fúria Espartana", "dano": 30, "custo_mana": 15},
                {"nome": "Ataque Rápido", "dano": 12, "custo_mana": 0}
            ]
        elif self.classe == "Arqueiro":
            return [
                {"nome": "Chuva de Flechas", "dano": 18, "custo_mana": 8},
                {"nome": "Tiro Preciso", "dano": 28, "custo_mana": 18},
                {"nome": "Disparo Duplo", "dano": 14, "custo_mana": 0}
            ]
        elif self.classe == "Paladino":
            return [
                {"nome": "Julgamento Divino", "dano": 22, "custo_mana": 12},
                {"nome": "Escudo de Luz", "dano": 15, "custo_mana": 5},
                {"nome": "Golpe Sagrado", "dano": 12, "custo_mana": 0}
            ]
        elif self.classe == "Assassino":
            return [
                {"nome": "Ataque Sombrio", "dano": 26, "custo_mana": 10},
                {"nome": "Apunhalada", "dano": 40, "custo_mana": 25},
                {"nome": "Corte Rápido", "dano": 11, "custo_mana": 0}
            ]


# ==========================================
# 2. SISTEMA DE COMBATE EM EQUIPE
# ==========================================
def exibir_status_combate(equipe, inimigo_nome, inimigo_vida, inimigo_vida_max):
    status_texto = ""
    
    # Status dos Heróis
    for heroi in equipe:
        if heroi.vida > 0:
            pct_vida = max(0, heroi.vida / heroi.vida_max)
            pct_mana = max(0, heroi.mana / heroi.mana_max)
            barra_vida = '●' * int(pct_vida * 10) + '○' * (10 - int(pct_vida * 10))
            barra_mana = '●' * int(pct_mana * 10) + '○' * (10 - int(pct_mana * 10))
            status_texto += (
                f"[bold green]⚔️ {heroi.nome.upper()}[/bold green] ({heroi.classe})\n"
                f"HP  : {heroi.vida}/{heroi.vida_max} [{barra_vida}]\n"
                f"MANA: {heroi.mana}/{heroi.mana_max} [{barra_mana}]\n\n"
            )
        else:
            status_texto += f"[bold red]💀 {heroi.nome.upper()} (DERROTADO)[/bold red]\n\n"
            
    # Status do Inimigo
    pct_vida_ini = max(0, inimigo_vida / inimigo_vida_max)
    barra_vida_ini = '●' * int(pct_vida_ini * 10) + '○' * (10 - int(pct_vida_ini * 10))
    status_texto += (
        f"----------------------------------------\n"
        f"[bold red]😈 INIMIGO: {inimigo_nome.upper()}[/bold red]\n"
        f"HP  : {inimigo_vida}/{inimigo_vida_max} [{barra_vida_ini}]"
    )
    
    console.print(Panel(status_texto, title="[bold yellow] STATUS DO COMBATE [/bold yellow]", border_style="cyan", expand=False))


def iniciar_combate(equipe, inimigo):
    inimigo_nome = inimigo["nome"]
    inimigo_vida_max = inimigo["vida"]
    inimigo_vida = inimigo_vida_max
    inimigo_ataque = inimigo["ataque"]

    console.print(Panel.fit(f" [bold red]⚔️ UM {inimigo_nome.upper()} BLOQUEIA SEU CAMINHO! (HP: {inimigo_vida_max} | ATK: {inimigo_ataque}) ⚔️[/bold red] ", border_style="red", padding=(1, 5)))
    time.sleep(1.5)

    while inimigo_vida > 0 and any(h.vida > 0 for h in equipe):
        exibir_status_combate(equipe, inimigo_nome, inimigo_vida, inimigo_vida_max)
        
        # Turno de cada Herói vivo
        for heroi in equipe:
            if heroi.vida <= 0:
                continue
            if inimigo_vida <= 0:
                break
                
            console.print(f"\n[bold green]➔ Turno de {heroi.nome} ({heroi.classe})[/bold green]")
            
            tabela_golpes = Table(title_style="bold magenta")
            tabela_golpes.add_column("Nº", justify="center", style="bold yellow")
            tabela_golpes.add_column("Habilidade", style="bold white")
            tabela_golpes.add_column("Dano", justify="right", style="bold red")
            tabela_golpes.add_column("Mana", justify="right", style="bold blue")

            for i, golpe in enumerate(heroi.golpes):
                tabela_golpes.add_row(str(i + 1), golpe['nome'], f"{golpe['dano']} DMG", f"{golpe['custo_mana']} MP")
            console.print(tabela_golpes)
            
            escolha = Prompt.ask(f"[bold yellow]Escolha o golpe de {heroi.nome}[/bold yellow]", choices=["1", "2", "3"])
            golpe_escolhido = heroi.golpes[int(escolha) - 1]
            
            if heroi.mana >= golpe_escolhido["custo_mana"]:
                heroi.mana -= golpe_escolhido["custo_mana"]
                dano_total = heroi.ataque_base + golpe_escolhido["dano"]
                inimigo_vida -= dano_total
                console.print(f"💥 [bold green]{heroi.nome} usou {golpe_escolhido['nome']} causando {dano_total} de dano![/bold green]")
            else:
                console.print("❌ [bold dark_orange]Sem mana! Soco básico desferido: 5 de dano.[/bold dark_orange]")
                inimigo_vida -= 5
            time.sleep(1)

        # Turno do Inimigo (Se ainda estiver vivo)
        if inimigo_vida > 0:
            herois_vivos = [h for h in equipe if h.vida > 0]
            alvo = random.choice(herois_vivos)
            alvo.vida -= inimigo_ataque
            console.print(f"\n👹 [bold red]O {inimigo_nome} contra-atacou focado em {alvo.nome} causando {inimigo_ataque} de dano![/bold red]")
            time.sleep(1.5)
            
    if any(h.vida > 0 for h in equipe):
        console.print(Panel.fit(f"🏆 [bold gold1]VITÓRIA! O {inimigo_nome} foi pulverizado![/bold gold1] 🏆", border_style="gold1"))
        for h in equipe:
            if h.vida > 0:
                h.mana = min(h.mana_max, h.mana + 20)
        return True
    else:
        console.print(Panel.fit("\n💀 GAME OVER! Sua equipe inteira foi massacrada nas profundezas da masmorra... 💀", border_style="red"))
        return False


# ==========================================
# 3. TELA DE CRIAÇÃO MULTIPERSONAGEM
# ==========================================
def criar_equipe():
    console.print(Panel(
        "[bold gold1]🧙‍♂️  BEM-VINDO AO REINO DE PYTHONIA  🧝‍♂️[/bold gold1]\n"
        "[dim]Monte sua guilda de 1 a 3 heróis para enfrentar o perigo.[/dim]",
        border_style="gold1", expand=False
    ))
    
    qtd_herois = int(Prompt.ask("[bold white]Quantos heróis deseja criar? (1 a 3)[/bold white]", choices=["1", "2", "3"]))
    equipe = []
    
    racas = ["Humano", "Elfo", "Anão", "Orc", "Draconato"]
    classes = ["Guerreiro", "Mago", "Arqueiro", "Paladino", "Assassino"]

    for idx in range(qtd_herois):
        console.print(f"\n[bold cyan]=== Criando o {idx+1}º Herói ===[/bold cyan]")
        nome = Prompt.ask("[bold white]Nome do Herói[/bold white]")
        
        # Tabela de Raças
        t_racas = Table(title="Raças Disponíveis", title_style="bold green")
        t_racas.add_column("ID", justify="center", style="bold yellow")
        t_racas.add_column("Raça", style="bold white")
        t_racas.add_column("Bônus", style="italic cyan")
        for i, r in enumerate(racas):
            t_racas.add_row(str(i+1), r, ["+2 ATK", "+25 MANA", "+30 HP", "+7 ATK", "+15 HP / +10 MP"][i])
        console.print(t_racas)
        esc_raca = Prompt.ask("Escolha o ID da Raça", choices=["1", "2", "3", "4", "5"])
        raca_sel = racas[int(esc_raca) - 1]

        # ==========================================
        # TABELA EXPLICATIVA DAS CLASSES (NOVA)
        # ==========================================
        t_info_classes = Table(title="📜 MANUAL DE CLASSES (LEIA ANTES DE ESCOLHER)", title_style="bold gold1")
        t_info_classes.add_column("Classe", style="bold white", justify="center")
        t_info_classes.add_column("Estilo de Jogo", style="cyan")
        t_info_classes.add_column("Vantagens", style="bold green")
        t_info_classes.add_column("Desvantagens", style="bold red")
        
        t_info_classes.add_row(
            "Guerreiro", 
            "Combatente de linha de frente resiliente.", 
            "Golpes potentes gastando pouquíssima mana.", 
            "Não possui golpes de altíssimo dano explosivo."
        )
        t_info_classes.add_row(
            "Mago", 
            "Mestre das artes arcanas e feitiçaria.", 
            "Dano em área massivo e capacidade de drenar mana.", 
            "Depende totalmente de mana; sem ela, fica inútil."
        )
        t_info_classes.add_row(
            "Arqueiro", 
            "Atirador preciso de longa distância.", 
            "Dano balanceado e habilidades de custo muito baixo.", 
            "Causa menos dano em alvos únicos que o Assassino."
        )
        t_info_classes.add_row(
            "Paladino", 
            "Defensor sagrado movido pela fé.", 
            "Habilidades mistas de proteção com custo de mana baixo.", 
            "Seu dano geral é mais contido e focado em resistência."
        )
        t_info_classes.add_row(
            "Assassino", 
            "Predador furtivo das sombras.", 
            "Tem o golpe de maior dano do jogo (Apunhalada: 40 DMG).", 
            "Esse golpe principal drena metade da sua barra de mana."
        )
        
        console.print("\n")
        console.print(t_info_classes)

        # Seleção de Classes normal
        t_classes = Table(title="Menu de Seleção", title_style="bold blue")
        t_classes.add_column("ID", justify="center", style="bold yellow")
        t_classes.add_column("Classe", style="bold white")
        for i, c in enumerate(classes):
            t_classes.add_row(str(i+1), c)
        console.print(t_classes)
        
        esc_classe = Prompt.ask("Escolha o ID da Classe com base no manual acima", choices=["1", "2", "3", "4", "5"])
        classe_sel = classes[int(esc_classe) - 1]

        heroi = Personagem(nome, raca_sel, classe_sel)
        equipe.append(heroi)
        console.print(f"[bold green]✓ {nome} o {classe_sel} foi adicionado à equipe![/bold green]")
        
    return equipe


# ==========================================
# 4. JORNADA PRINCIPAL (CAMPANHA)
# ==========================================
if __name__ == "__main__":
    console.clear()
    sua_equipe = criar_equipe()
    
    # Lista de 5 Batalhas Progressivas
    masmorra_monstros = [
        {"nome": "Goblin Larápio", "vida": 50, "ataque": 10},
        {"nome": "Lobo Atroz", "vida": 75, "ataque": 14},
        {"nome": "Orc Saqueador", "vida": 110, "ataque": 18},
        {"nome": "Gárgula de Pedra", "vida": 150, "ataque": 22},
        {"nome": "Quimera de Fogo", "vida": 200, "ataque": 28}
    ]
    
    # O Chefão Final
    boss_final = {"nome": "Nefarian, O Dragão Ancião de Pythonia", "vida": 450, "ataque": 40}
    
    Prompt.ask("\n[bold blink cyan]Sua equipe está pronta. Pressione ENTER para marchar em direção às 5 Batalhas...[/bold blink cyan]")
    
    jornada_vitoriosa = True
    
    # Loop das 5 batalhas normais
    for idx, monstro in enumerate(masmorra_monstros):
        console.clear()
        console.print(Panel(f"[bold yellow]ETAPA {idx+1} / 5[/bold yellow]\nDescendo mais fundo na escuridão...", border_style="yellow"))
        
        vitoria = iniciar_combate(sua_equipe, monstro)
        if not vitoria:
            jornada_vitoriosa = False
            break
            
        Prompt.ask("\n[bold green]Inimigo derrotado! Pressione ENTER para prosseguir...[/bold green]")

    # Se passou das 5 batalhas, enfrenta o BOSS FINAL
    if jornada_vitoriosa:
        console.clear()
        console.print(Panel(
            "[bold flash red]☠️ ALERTA DE CHEFÃO FINAL ☠️[/bold flash red]\n"
            "O chão treme, as paredes derretem... A criatura suprema acordou!",
            border_style="red"
        ))
        Prompt.ask("\n[bold blink red]PREPARE SEU CORAÇÃO... Pressione ENTER para a Batalha Final![/bold blink red]")
        console.clear()
        
        vitoria_final = iniciar_combate(sua_equipe, boss_final)
        if vitoria_final:
            console.clear()
            console.print(Panel(
                "[bold gold1]👑 OS LENDÁRIOS SALVADORES DE PYTHONIA! 👑[/bold gold1]\n"
                "Você completou o desafio, limpou as 5 hordas e baniu o Dragão Ancião para sempre!\n"
                "O reino celebra sua glória eterna!",
                border_style="gold1", padding=2
            ))