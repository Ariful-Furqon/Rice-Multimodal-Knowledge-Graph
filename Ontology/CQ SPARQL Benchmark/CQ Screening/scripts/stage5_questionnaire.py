"""
Stage 5 of the CQ screening funnel: build the blinded expert questionnaire.

Three things happen here.

NO SAMPLING IS NEEDED. Stage 3 produced 23 canonical CQs and the planned
questionnaire size was 30-50 items, so every CQ goes in. The earlier worry --
that a convergence-ranked cut would leave only high-`n_models` CQs and make the
hypothesis *does convergence predict expert-rated relevance* untestable -- does
not arise: all nine single-model CQs are included alongside the six proposed
by four models, giving the full spread the analysis needs.

INSTANTIATION. 54 of the 173 pooled CQs were templates (*a given disease*, *N
days*). An expert cannot judge whether "which pathogen causes a given disease"
is agronomically sound; they can judge "which pathogen causes rice blast". Each
item below is therefore instantiated with an entity that actually exists in
RiceMMKG v0.6, so the question is answerable in principle and the expert is
rating something concrete.

BLINDING. Item order is shuffled with a fixed seed, and the questionnaire shows
no source model, no `n_models`, no group id, and no benchmark-corroboration
flag. Those live only in the key file. If a rater could see that four models
proposed an item, their rating would no longer be independent evidence about
convergence -- which is the one thing this instrument exists to test.

Outputs:
  ../data/cq_stage5_items.csv       blinded items, in presentation order
  ../data/cq_stage5_key.csv         unblinding key -- do not show to raters
  ../data/cq_stage5_responses.csv   empty response template, one row per rating
  ../reports/cq_stage5_questionnaire.md  the form to hand to experts (Indonesian)
"""

import csv
import random
import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
DATA = ROOT / "data"
REPORTS = ROOT / "reports"

SHUFFLE_SEED = 20260907   # fixed so the running order is reproducible

# Number of experts the response template is laid out for. Two is the minimum
# for an agreement coefficient; three makes a disagreement interpretable.
N_EXPERTS = 3

# cq_id -> (instantiated English question, instantiated Indonesian question)
# Entities are drawn from RiceMMKG v0.6, so each item is answerable in principle.
ITEMS = {
    "CQ-A01": (
        "Which pathogen causes Rice Blast, and to which taxonomic group "
        "(fungus, bacterium, virus) does it belong?",
        "Patogen apa yang menyebabkan penyakit blas (rice blast), dan termasuk "
        "kelompok taksonomi apa (jamur, bakteri, virus)?"),
    "CQ-A02": (
        "Which vector species transmits Rice Tungro Bacilliform Virus, and by "
        "which transmission mode?",
        "Spesies vektor apa yang menularkan Rice Tungro Bacilliform Virus, dan "
        "melalui mekanisme penularan apa?"),
    "CQ-A03": (
        "Which symptoms does Bacterial Leaf Blight produce, on which plant "
        "organ, and at which growth stage?",
        "Gejala apa saja yang ditimbulkan hawar daun bakteri (bacterial leaf "
        "blight), pada organ tanaman apa, dan pada fase pertumbuhan apa?"),
    "CQ-A04": (
        "Which diseases share symptoms with Brown Spot, and which symptoms "
        "discriminate between them?",
        "Penyakit apa saja yang gejalanya tumpang tindih dengan bercak coklat "
        "(brown spot), dan gejala apa yang membedakannya?"),
    "CQ-A05": (
        "Which environmental conditions are reported to favour Sheath Blight?",
        "Kondisi lingkungan apa yang dilaporkan memicu berkembangnya hawar "
        "pelepah (sheath blight)?"),
    "CQ-A06": (
        "At which growth stages is Brown Planthopper reported as most damaging?",
        "Pada fase pertumbuhan apa wereng batang coklat dilaporkan paling "
        "merusak?"),
    "CQ-A07": (
        "Which control measures are recommended for Stem Borer, of which "
        "management category (chemical, biological, cultural), and on which "
        "source authority?",
        "Tindakan pengendalian apa yang direkomendasikan untuk penggerek "
        "batang, termasuk kategori apa (kimiawi, hayati, kultur teknis), dan "
        "bersumber dari rujukan apa?"),
    "CQ-A08": (
        "Which natural enemies are documented as predators or parasitoids of "
        "Brown Planthopper?",
        "Musuh alami apa saja yang tercatat sebagai predator atau parasitoid "
        "wereng batang coklat?"),
    "CQ-A09": (
        "Which features distinguish a nutritional disorder such as zinc "
        "deficiency from Rice Blast, when the visible symptoms are similar?",
        "Ciri apa yang membedakan gangguan hara seperti defisiensi seng dari "
        "penyakit blas, ketika gejala yang tampak mirip?"),
    "CQ-A10": (
        "Which images are annotated as showing Hispa damage?",
        "Citra mana saja yang dianotasi menunjukkan serangan hispa?"),
    "CQ-A11": (
        "Who or what produced the annotation of a given image, and with what "
        "confidence?",
        "Siapa atau apa yang membuat anotasi pada suatu citra, dan dengan "
        "tingkat keyakinan berapa?"),
    "CQ-A12": (
        "On which conditions do model-generated and expert image annotations "
        "disagree?",
        "Pada kondisi apa saja anotasi hasil model dan anotasi pakar berbeda?"),
    "CQ-A13": (
        "How many images exist for each condition, plant organ, and capture "
        "type (field versus close-up)?",
        "Berapa jumlah citra untuk tiap kondisi, organ tanaman, dan jenis "
        "pengambilan (lapangan atau jarak dekat)?"),
    "CQ-A14": (
        "Which plant organ (leaf, sheath, stem, panicle) is depicted in a given "
        "image?",
        "Organ tanaman apa (daun, pelepah, batang, malai) yang tampak pada "
        "suatu citra?"),
    "CQ-A15": (
        "Which visible symptoms are annotated in a given image?",
        "Gejala apa saja yang dianotasi pada suatu citra?"),
    "CQ-A16": (
        "Which disease or pest is best supported by the visual evidence in an "
        "image showing brown lesions on the leaf blade?",
        "Penyakit atau hama apa yang paling didukung oleh bukti visual pada "
        "citra yang menunjukkan bercak coklat di helai daun?"),
    "CQ-A17": (
        "Which visual features separate Brown Spot from Rice Blast?",
        "Ciri visual apa yang membedakan bercak coklat (brown spot) dari "
        "penyakit blas (rice blast)?"),
    "CQ-A18": (
        "How severe is the damage recorded in a given image?",
        "Seberapa berat tingkat kerusakan yang tercatat pada suatu citra?"),
    "CQ-A19": (
        "Which symptoms co-occur on the same plant within a single image?",
        "Gejala apa saja yang muncul bersamaan pada satu tanaman dalam satu "
        "citra?"),
    "CQ-A20": (
        "Which growth stage is visually manifest in a whole-canopy image?",
        "Fase pertumbuhan apa yang tampak dari citra kanopi utuh?"),
    "CQ-A21": (
        "Which symptoms described in the literature have supporting image "
        "evidence, and which do not?",
        "Gejala apa yang dideskripsikan di literatur dan memiliki bukti citra "
        "pendukung, dan mana yang tidak?"),
    "CQ-A22": (
        "Which disease described in the literature matches the symptoms "
        "annotated in an image showing water-soaked streaks?",
        "Penyakit apa dalam literatur yang cocok dengan gejala teranotasi pada "
        "citra yang menunjukkan garis kebasahan (water-soaked streak)?"),
    "CQ-A23": (
        "Which treatment does the literature prescribe for a condition "
        "identified from an image as Sheath Blight?",
        "Tindakan apa yang direkomendasikan literatur untuk kondisi yang "
        "teridentifikasi dari citra sebagai hawar pelepah?"),
}


def main():
    canonical = list(csv.DictReader(
        (DATA / "cq_stage3_final_tierA.csv").open(encoding="utf-8-sig")))
    assert set(ITEMS) == {c["cq_id"] for c in canonical}, \
        "ITEMS out of sync with the final CQ set"

    corroborated = set()
    recon = DATA / "cq_stage4_reconciliation.csv"
    if recon.exists():
        for r in csv.DictReader(recon.open(encoding="utf-8-sig")):
            corroborated.update(r["maps_to"].split())

    order = list(canonical)
    random.Random(SHUFFLE_SEED).shuffle(order)

    items, key = [], []
    for n, c in enumerate(order, start=1):
        en, idn = ITEMS[c["cq_id"]]
        items.append({"item_no": n, "question_id": idn, "question_en": en})
        key.append({"item_no": n,
                    "cq_id": c["cq_id"],
                    "level": c["level"],
                    "dim": c["dim"],
                    "category": c["category"],
                    "n_models": c["n_models"],
                    "benchmark_corroborated":
                        "yes" if c["cq_id"] in corroborated else "no",
                    "v06_status": c["v06_status"],
                    "canonical_question": c["canonical_question"]})

    # The form is the deliverable, so write it first: a spreadsheet left open
    # in Excel should not be able to block it.
    write_form(items)

    responses = [{"item_no": i["item_no"], "expert_id": f"E{e}",
                  "relevance_1_5": "", "clarity_1_5": "", "comment": ""}
                 for e in range(1, N_EXPERTS + 1) for i in items]
    responses.sort(key=lambda r: (r["expert_id"], r["item_no"]))

    write_csv(DATA / "cq_stage5_items.csv", items)
    write_csv(DATA / "cq_stage5_key.csv", key)
    write_csv(DATA / "cq_stage5_responses.csv", responses)
    print(f"questionnaire: {len(items)} items, seed {SHUFFLE_SEED}, "
          f"response template for {N_EXPERTS} experts")
    print(f"  key kept separately in {DATA.name}/cq_stage5_key.csv "
          "- do not give this to raters")


def write_csv(path, rows):
    try:
        f = path.open("w", encoding="utf-8-sig", newline="")
    except PermissionError:
        raise SystemExit(
            f"\n{path.name} is locked - close it in Excel and run again.\n"
            "(The questionnaire itself was written; only this file is stale.)")
    with f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def write_form(items):
    L = ["# Kuesioner Validasi Pakar",
         "## Pertanyaan Kompetensi untuk Knowledge Graph Hama dan Penyakit Padi",
         "",
         f"*Versi {datetime.datetime.now():%Y-%m-%d}. "
         f"{len(items)} pertanyaan.*", "",
         "---", "", "## Pengantar", "",
         "Kami sedang **merancang** sebuah basis pengetahuan (*knowledge "
         "graph*) tentang hama dan penyakit padi, yang akan menggabungkan "
         "pengetahuan dari literatur dengan citra gejala di lapangan.", "",
         "Tahap yang sedang kami kerjakan adalah **penentuan cakupan**: "
         "menetapkan pertanyaan-pertanyaan apa saja yang nantinya harus dapat "
         "dijawab. Dalam rekayasa ontologi, daftar semacam ini disebut "
         "*competency questions* dan berfungsi sebagai spesifikasi kebutuhan - "
         "ditetapkan **sebelum** sistemnya dibangun, dan menentukan entitas "
         "serta relasi apa yang perlu direpresentasikan.", "",
         "**Belum ada sistem yang perlu Anda coba, dan Anda tidak perlu "
         "menjawab pertanyaan-pertanyaannya.** Yang kami minta adalah "
         "penilaian Anda sebagai pakar atas pertanyaannya sendiri:", "",
         "- Apakah pertanyaan ini penting dalam praktik diagnosis dan "
         "pengelolaan hama serta penyakit padi?",
         "- Apakah rumusannya sudah tepat menurut peristilahan di lapangan, "
         "dan tidak menimbulkan tafsir ganda?", "",
         "Penilaian Anda menentukan bagian mana dari basis pengetahuan ini "
         "yang kami bangun lebih dahulu, dan mana yang kami tunda.", "",
         "Pengisian diperkirakan memakan waktu 20-30 menit.", "",
         "## Cara mengisi", "",
         "Untuk setiap pertanyaan, berikan dua penilaian pada skala 1-5:", "",
         "**Relevansi** - seberapa penting pertanyaan ini bagi praktik "
         "diagnosis dan pengelolaan hama serta penyakit padi?", "",
         "| 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|",
         "| tidak relevan | kurang relevan | cukup | penting | sangat penting |",
         "",
         "**Kejelasan** - apakah pertanyaan ini dirumuskan dengan jelas dan "
         "tidak menimbulkan tafsir ganda?", "",
         "| 1 | 2 | 3 | 4 | 5 |", "|---|---|---|---|---|",
         "| sangat kabur | kabur | cukup | jelas | sangat jelas |", "",
         "Kolom **catatan** bersifat opsional. Mohon diisi terutama bila Anda "
         "memberi nilai rendah, atau bila istilah yang kami gunakan keliru "
         "menurut praktik di lapangan.", "",
         "---", "", "## Daftar pertanyaan", ""]

    for it in items:
        L += [f"### {it['item_no']}. {it['question_id']}", "",
              f"<sub>{it['question_en']}</sub>", "",
              "| Relevansi (1-5) | Kejelasan (1-5) | Catatan |",
              "|---|---|---|", "|  |  |  |", ""]

    L += ["---", "", "## Bagian akhir: pertanyaan yang belum tercakup", "",
          "Bagian ini sama pentingnya dengan penilaian di atas. Daftar tersebut "
          "kami susun dari sumber otomatis, sehingga besar kemungkinan ada hal "
          "yang penting di lapangan namun tidak muncul di sana.", "",
          "**Menurut Anda, pertanyaan apa yang seharusnya masuk dalam cakupan "
          "basis pengetahuan ini, tetapi belum ada dalam daftar di atas?**", ""]
    for i in range(1, 6):
        L += [f"{i}. ", "", "&nbsp;", ""]
    L += ["---", "", "## Identitas penilai", "",
          "| | |", "|---|---|",
          "| Nama | |", "| Institusi | |",
          "| Bidang keahlian | |",
          "| Lama pengalaman di bidang padi (tahun) | |",
          "| Tanggal pengisian | |", "",
          "Terima kasih atas waktu dan penilaian Anda.", ""]

    (REPORTS / "cq_stage5_questionnaire.md").write_text("\n".join(L),
                                                        encoding="utf-8")


if __name__ == "__main__":
    main()
