level_manager = None
sound_manager = None
scene_manager = None

# MULTIPLIERS
better_eyesight = False
gold_mult = 1
legday_mult = 1
lifesteal_mult = 0
player_max_health = 1000
acid_blood_mult = 0
bleeding = 0
soul_collector = False
soul_eater = False
soul_blast = False
damage_mult = 1
knockback_mult = 1
resistance_mult = 1

def reset_multipliers():
    global better_eyesight, gold_mult, legday_mult, lifesteal_mult, player_max_health, acid_blood_mult, bleeding, soul_collector, soul_eater, soul_blast, damage_mult, knockback_mult, resistance_mult
    better_eyesight = False
    gold_mult = 1
    legday_mult = 1
    lifesteal_mult = 0
    player_max_health = 1000
    acid_blood_mult = 0
    bleeding = 0
    soul_collector = False
    soul_eater = False
    soul_blast = False
    damage_mult = 1
    knockback_mult = 1
    resistance_mult = 1