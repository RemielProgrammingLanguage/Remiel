# 🧠 Remiel Programming Language

**Remiel** is a new programming language designed for the future — built from the ground up to support **AI**, **game development**, **neural systems**, and **blockchain** all in one unified syntax.

> Created by **Remiel Halliday (Kibirango Asuman)**  
> Developed under the **Neuron Innovation Team**  
> Powered by the **Neuron Innovation Network**

---

## 🚀 Vision

Remiel isn't just another general-purpose language — it's a **multi-paradigm DSL-style language** that gives developers tools to:

- Build **AI agents** and train neural networks natively
- Design **game worlds**, entities, and simulation logic with event-based syntax
- Deploy and interact with **smart contracts** and crypto wallets easily
- Handle **system logic, data, and events** in a modular and readable way

---

## 💎 Features

- `strict_mode`, `universal_mode`, `dynamic_mode` — choose your typing discipline
- Native constructs for:
  - AI systems: `ai`, `network`, `.predict`, `train`
  - Blockchain: `contract`, `wallet`, `send`, `coin`
  - Games & Simulations: `entity`, `event`, `trigger`, `loop`
  - File & Storage systems: `save`, `load`, `list_files`, `delete`
  - Modular structure: `bring from [...]` for imports
- Clear, readable syntax focused on expressiveness and accessibility

---

## 🧪 Current Status

> Remiel is in **active MVP development**. We're building the core syntax, interpreter, and standard library — and seeking feedback from early testers.

If you're a developer passionate about:
- Language design
- Systems programming
- AI/game/blockchain integration
- Building futuristic dev tools

We'd love your thoughts, ideas, or collaboration.

---

## 📂 Example Syntax

```remiel
strict_mode

entity Player
  natural keep health = 100
  list of point keep position = [0.0, 0.0]
end

on 'player_damage'
  trigger Player.health -= 10
end

contract Store
  natural keep item_price = 5
  define buy [wallet]
    check (wallet.balance >= item_price)
      send item_price coin from [wallet] to [this]
  end
end
