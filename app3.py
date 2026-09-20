import streamlit as st

# ==========================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="KWS Ranger: Life on Land",
    page_icon="🌍",
    layout="centered"
)

# ==========================================
# BANCO DE PERGUNTAS (ODS 15)
# ==========================================
QUESTIONS = [
    # Stage 1: Mau Forest
    {
        "q": "What is currently the biggest threat to land animals and plants?",
        "options": [
            "Noise pollution from cities and cars.",
            "Habitat loss, mainly because people clear forests for farming and building.",
            "Natural changes in the sun's temperature."
        ],
        "ans": 1,
        "exp": "Most of the land on Earth has been changed by human activity. When we destroy forests, animals lose their homes and struggle to survive."
    },
    {
        "q": "Trees store a lot of carbon. What happens when a large forest is cut down or burned?",
        "options": [
            "The carbon goes into the soil and stays there safely.",
            "The stored carbon is released into the air, making climate change worse.",
            "The carbon turns into water vapor."
        ],
        "ans": 1,
        "exp": "Forests help control the climate. When trees are destroyed, all the carbon they absorbed goes back into the atmosphere."
    },
    {
        "q": "Why is illegal hunting so dangerous for large animals like rhinos and elephants?",
        "options": [
            "Because they refuse to eat if they are stressed by hunters.",
            "Because they have very few babies, and hunters kill them faster than they can reproduce.",
            "Because they forget how to survive in the wild."
        ],
        "ans": 1,
        "exp": "These animals take a long time to grow and have offspring. Hunting easily wipes out their entire population."
    },
    # Stage 2: Mount Kenya Slopes
    {
        "q": "What happens when a new road or farm cuts a large forest into smaller pieces?",
        "options": [
            "It isolates animal groups, making it harder for them to find food and new mates.",
            "It helps animals because they can use the roads to travel faster.",
            "It automatically makes the forest grow quicker."
        ],
        "ans": 0,
        "exp": "This is called habitat fragmentation. When animal groups are separated, they can't travel safely and their population gets weaker."
    },
    {
        "q": "Pangolins are often captured illegally. Why are they so important to the environment?",
        "options": [
            "They carry heavy seeds from the river to the mountains.",
            "They eat millions of ants and termites, keeping the insect population under control.",
            "They pollinate the flowers in the highest trees."
        ],
        "ans": 1,
        "exp": "A single pangolin eats a huge amount of insects every year. Without them, ants and termites could damage the ecosystem."
    },
    {
        "q": "Why do conservationists try to build 'wildlife corridors' between nature reserves?",
        "options": [
            "So tourists can drive between parks without getting lost.",
            "To connect broken habitats, allowing animals to travel safely and find resources.",
            "To keep park rangers away from dangerous areas."
        ],
        "ans": 1,
        "exp": "Wildlife corridors are like safe bridges of land. They let animals move between protected areas without crossing dangerous roads or farms."
    },
    # Stage 3: Samburu Reserve
    {
        "q": "People still hunt the Black Rhino illegally. Why does this happen?",
        "options": [
            "Because people buy their horns on the black market, believing they have medical value.",
            "Because their horns are used to build modern computer parts.",
            "Because they are a threat to big cities."
        ],
        "ans": 0,
        "exp": "Rhino horns are just made of keratin, the same stuff as our hair and nails. They have no medical value, but the illegal trade still threatens them."
    },
    {
        "q": "Wild monkeys play a big role in the forest. How do they help the ecosystem?",
        "options": [
            "They stop tall trees from growing too fast.",
            "They eat fruit and drop the seeds everywhere, helping new plants grow across the forest.",
            "They chase away invasive bird species."
        ],
        "ans": 1,
        "exp": "Monkeys act like natural gardeners. By dropping seeds far away from the parent tree, they help the forest regenerate."
    },
    {
        "q": "What does it mean when an animal is called a 'keystone species'?",
        "options": [
            "It means they have the most babies every year.",
            "It means the whole ecosystem depends on them, and things would fall apart if they disappear.",
            "It means they are easy to domesticate."
        ],
        "ans": 1,
        "exp": "A keystone holds an arch together. In nature, a keystone species keeps the environment balanced. Without them, the habitat changes completely."
    },
    {
        "q": "How can local communities help protect nature and support SDG 15?",
        "options": [
            "By cutting down native trees and planting foreign grass.",
            "By getting involved in conservation and eco-tourism, protecting animals while helping their own economy.",
            "By building tall fences around all the rivers."
        ],
        "ans": 1,
        "exp": "When local people are part of the solution, they protect the wildlife because a healthy environment also supports their community."
    }
]

# Mensagens mais simples e reais quando a equipe perde membros
TEAM_DAMAGE_MESSAGES = [
    "Sergeant Kwame got hit in his vest. He needs to fall back. Be careful!",
    "Officer Nia twisted her ankle trying to get a better view. She's out of this operation.",
    "A poacher shot out the jeep's tire. Officer Jabari is staying behind to fix it.",
    "Officer Zuri is pinned down trying to help a trapped animal. You have to finish this alone."
]

# ==========================================
# GERENCIAMENTO DE ESTADO (SESSION STATE)
# ==========================================
def init_game():
    st.session_state.current_stage = 0
    st.session_state.player_hp = 8
    st.session_state.enemy_hp = 3
    st.session_state.q_index = 0
    st.session_state.team = ["Sergeant Kwame", "Officer Nia", "Officer Jabari", "Officer Zuri"]
    st.session_state.feedback = ""
    st.session_state.damage_msg = ""
    st.session_state.game_over = False
    st.session_state.victory = False

if 'current_stage' not in st.session_state:
    init_game()

# ==========================================
# FUNÇÕES DE LÓGICA E INTERAÇÃO
# ==========================================
def process_answer(selected_idx, correct_idx, explanation):
    st.session_state.damage_msg = ""
   
    if selected_idx == correct_idx:
        st.session_state.enemy_hp -= 1
        st.session_state.feedback = f"✅ **Correct!** {explanation}"
    else:
        st.session_state.player_hp -= 1
        st.session_state.feedback = f"❌ **Incorrect.** {explanation}"
       
        # Remoção de membro da equipe a cada 2 HP perdidos
        hp = st.session_state.player_hp
        if hp in [6, 4, 2, 0] and len(st.session_state.team) > 0:
            st.session_state.team.pop(0)
            msg_index = min(3, 3 - len(st.session_state.team))
            st.session_state.damage_msg = TEAM_DAMAGE_MESSAGES[msg_index]
           
        if hp <= 0:
            st.session_state.game_over = True
            st.session_state.current_stage = "Defeat"
            return

    # Progresso de Fases
    if st.session_state.enemy_hp <= 0:
        st.session_state.current_stage += 1
       
        if st.session_state.current_stage == 2:
            st.session_state.enemy_hp = 3
            st.session_state.feedback += "\n\n📻 **Radio:** *The camp is secure. We have reports of smugglers heading up Mount Kenya. Go there now.*"
        elif st.session_state.current_stage == 3:
            st.session_state.enemy_hp = 4
            st.session_state.feedback += "\n\n📻 **Radio:** *Good job on the mountain. We have an emergency at Samburu Reserve. A large group is attacking the rhinos.*"
        elif st.session_state.current_stage > 3:
            st.session_state.victory = True
            st.session_state.current_stage = "Victory"

    st.session_state.q_index = (st.session_state.q_index + 1) % len(QUESTIONS)

def render_ui_header(title):
    st.title(title)
   
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"💚 **Your HP:** {st.session_state.player_hp}/8")
    with col2:
        st.error(f"⚠️ **Poachers HP:** {st.session_state.enemy_hp}")
   
    if st.session_state.team:
        team_str = ", ".join([f"**{member}**" for member in st.session_state.team])
    else:
        team_str = "*You are alone now.*"
       
    st.markdown(f"👥 **Team with you ({len(st.session_state.team)}/4):** {team_str}")
    st.divider()

# ==========================================
# BARRA LATERAL (SIDEBAR)
# ==========================================
with st.sidebar:
    st.header("KWS Radio")
    if 'player_name' in st.session_state and st.session_state.player_name:
        st.markdown(f"👤 **Ranger:** {st.session_state.player_name}")
        st.markdown("🎯 **Mission Objective:** Protect wildlife and biodiversity")
        st.markdown("🌍 **UN Goal:** SDG 15 — Life on Land")
    st.write("---")
    if st.button("🔄 Restart Game", use_container_width=True):
        init_game()
        st.rerun()

# ==========================================
# FLUXO DAS TELAS NARRATIVAS
# ==========================================
stage = st.session_state.current_stage

if stage == 0:
    st.title("🌍 KWS Ranger: Life on Land")
    st.markdown("""
    Welcome to the bustling headquarters of the Kenya Wildlife Service (KWS). The air smells of morning coffee and the dry dust of the savanna. On the large wall map, red pins mark areas of recent illegal activity.
   
    Right now, poachers are capturing wild animals and destroying habitats to make illegal money.
    **Your objective is to save the animals and preserve life.** You must answer the questions correctly to deal damage to the traffickers and win the game.
   
    This mission is directly tied to the **UN's Sustainable Development Goal 15 (Life on Land)**.
    """)
       
    st.info("💡 Make the right choices to stop the poachers. If you make mistakes, members of your team might get hurt.")
   
    player_name = st.text_input("What is your name, Ranger?")
    if st.button("Start Mission", use_container_width=True):
        if player_name.strip():
            st.session_state.player_name = player_name.strip()
            st.session_state.current_stage = 1
            st.rerun()
        else:
            st.warning("Please type your name before starting.")

elif stage == 1:
    render_ui_header("🌲 Stage 1: Mau Forest")
    st.markdown(f"""
    You, Ranger **{st.session_state.player_name}**, are driving your jeep through the dense Mau Forest. The canopy above is so thick that only thin spears of sunlight pierce through the emerald darkness. The air is heavy with humidity, smelling of damp earth and rotting leaves.
   
    As your jeep struggles through the deep, sticky mud, Officer Nia gestures for silence. She points at fresh, deep tire tracks cutting through a bed of crushed ferns. Leaving the vehicles behind, you follow the trail on foot.
   
    Hidden beneath massive, moss-covered tree roots, you uncover a sprawling poacher camp. Rusty iron cages are stacked haphazardly in the mud. Inside, vibrant **African Grey Parrots** flutter in panic, while terrified **Pangolins** curl tightly into scaly balls in the corners of their traps, ready to be sold illegally. You unholster your tranquilizer and signal your team. You need to act now to free them.
    """)

elif stage == 2:
    render_ui_header("⛰️ Stage 2: Mount Kenya Slopes")
    st.markdown(f"""
    Ranger **{st.session_state.player_name}**, the mission intensifies. Your convoy climbs the treacherous, rocky paths of Mount Kenya. The air grows thin and biting cold. Frost clings to the sparse, thorny vegetation, and a thick, grey fog rolls down the jagged peaks, reducing your visibility to almost zero.
   
    Suddenly, your radio crackles through the howling wind with a tip: smugglers are navigating this rugged terrain to move a group of young **Cheetah Cubs** and ancient, massive **Giant Tortoises**. They are heading towards a secret, makeshift dirt runway hidden just above the cloud line.
   
    You can hear the distant, sputtering engines of a rusted cargo plane preparing for takeoff. The terrain is unforgiving and slippery with ice. Coordinate with your team, watch your footing, and make the right tactical choices to intercept them before that plane leaves the ground.
    """)

elif stage == 3:
    render_ui_header("🔥 Final Stage: Samburu Reserve")
    st.markdown(f"""
    Ranger **{st.session_state.player_name}**, there's no time to rest. An urgent distress signal comes through the radio. A massive, coordinated attack is happening right now in the Samburu Reserve.
   
    You arrive by helicopter, stepping out into a suffocating wave of heat. The reserve stretches out in a vast, sun-baked expanse of red dust and golden acacia trees. The horizon shimmers with a mirage, but the chaos ahead is terrifyingly real.
   
    A heavily armed group of poachers has cornered a majestic herd of **Black Rhinos** against a dry, cracked riverbed. The air is filled with the roar of heavy truck engines, shouting men, and the panicked, deafening cries of **Wild Monkeys** trapped in wooden crates loaded onto flatbeds. The red dust chokes your lungs as you and your team take cover behind a termite mound. This is a delicate and explosive situation. Think carefully about your actions to secure the area and protect these ancient creatures!
    """)

elif stage == "Victory":
    st.balloons()
    st.title("🏆 Mission Complete!")
    st.success(f"Great work, Ranger {st.session_state.player_name}!")
   
    st.markdown("""
    **Congratulations, you won the game and saved the animals' lives!**
   
    You managed to stop the poachers, dismantle their camps, and safely release the terrified animals back into their natural habitats. Protecting wildlife and their environments is exactly what **SDG 15 — Life on Land** is about. It's not just about winning a fight; it's about keeping the delicate ecosystem balanced so animals and humans can thrive together.
    """)
   
    st.write(f"📊 **Final Health:** {st.session_state.player_hp}/8 HP")
   
    if st.session_state.player_hp == 8:
        st.markdown("🌟 **FLAWLESS OPERATION!** You completed the mission without making a single mistake. Your tactical decisions were perfect, and your whole team returns home safe.")
       
    st.divider()
    if st.button("🎮 Play Again (Next Player)", use_container_width=True):
        init_game()
        st.rerun()

elif stage == "Defeat":
    st.title("💔 Mission Failed")
    st.error(f"You took too much damage, Ranger {st.session_state.player_name}.")
    st.markdown("""
    You and your team were overwhelmed and had to retreat to safety. The poachers managed to escape into the wilderness with the captured animals.
   
    Conservation is dangerous and difficult work, and sometimes things go wrong in the field. But learning about the environment and analyzing our mistakes is the first step to protecting it better next time. Review what happened, regroup, and try again.
    """)
    st.divider()
    if st.button("🔄 Try Again", use_container_width=True):
        init_game()
        st.rerun()

# ==========================================
# RENDERIZAÇÃO DO QUIZ
# ==========================================
if isinstance(stage, int) and stage > 0:
    if st.session_state.damage_msg:
        st.warning(f"⚠️ **TEAM UPDATE:** {st.session_state.damage_msg}")
    if st.session_state.feedback:
        st.info(st.session_state.feedback)
       
    st.divider()
   
    q_data = QUESTIONS[st.session_state.q_index]
   
    st.markdown("### 🎯 What do you know about this?")
    st.markdown(f"**{q_data['q']}**")
   
    for idx, option_text in enumerate(q_data["options"]):
        st.button(
            option_text,
            key=f"btn_stg{stage}_q{st.session_state.q_index}_opt{idx}",
            use_container_width=True,
            on_click=process_answer,
            args=(idx, q_data["ans"], q_data["exp"])
        )