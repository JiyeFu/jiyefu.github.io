---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<div class="landing-hero" markdown="1">
<span class='anchor' id='about-me'></span>
<div class="landing-hero__eyebrow">Computational Biology • Bioinformatics • Single-Cell Genomics</div>

I am a Postdoctoral Scholar at The Ohio State University (OSU). I received my Ph.D. in Biomedical Engineering from Southeast University (China) in 2025, where I was part of the State Key Laboratory of Digital Medical Engineering.

My research focuses on the intersection of Bioinformatics, Machine Learning, and Single-Cell Genomics. I am particularly interested in developing computational frameworks to decode complex genomic structures, such as G-quadruplexes (G4), and building large-scale data resources like the Human Single-Cell Genome Database (HSCGD). My work combines "dry-lab" expertise in machine learning (Python/R) with a solid foundation in "wet-lab" molecular techniques and nanopore sensing. My goal at OSU is to leverage these multi-disciplinary tools to further explore genomic adaptations and their implications in human health and disease.
</div>

<div class="section-card section-card--news" data-label="Recent update" markdown="1">
<span class='anchor' id='news'></span>
# 🔥 News
- *2026.02.23*: &nbsp;Excited to join the [BMBL](https://u.osu.edu/bmbl/) and [MaTRIX](https://u.osu.edu/matrix/) teams at OSU.
</div>

<div class="section-card section-card--experience" data-label="Current path" markdown="1">
<span class='anchor' id='professional-experience'></span>
# 💻 Professional Experience
- *2026.02 - present*, Postdoctoral Scholar in Computational Biology, The Ohio State University, Columbus, OH, USA.
- *2025.07 - 2025.12*, Research Assistant, Southeast University, Nanjing, China.
</div>

<div class="section-card section-card--education" data-label="Training" markdown="1">
<span class='anchor' id='education'></span>
# 📖 Education
- *2019.09 - 2025.06*, Ph.D. in Biomedical Engineering, Southeast University, Nanjing, China.
- *2016.09 - 2019.06*, M.S. in Biomedical Engineering, Southeast University, Nanjing, China.
- *2013.09 - 2016.06*, B.S. in Biomedical Engineering, Northeastern University, Shenyang, China.
</div>

<div class="section-card section-card--publications" data-label="Research output" markdown="1">
<span class='anchor' id='publications'></span>
# 📝 Publications 

<div class="featured-publications">
  <article class="featured-paper">
    <div class="featured-paper__meta">Featured Paper • 2025</div>
    <h3 class="featured-paper__title"><a href="https://www.mdpi.com/1422-0067/26/20/10025">Non-Random Distribution of G-Quadruplex Structures Reveals Regulatory and Ecological Adaptations in Bacterial Genomes</a></h3>
    <p class="featured-paper__venue"><strong>International Journal of Molecular Sciences</strong>, 2025</p>
    <div class="featured-paper__tags">
      <span>Bacterial Genomes</span>
      <span>G-Quadruplexes</span>
      <span>Genome Regulation</span>
    </div>
  </article>

  <article class="featured-paper">
    <div class="featured-paper__meta">Featured Paper • 2025</div>
    <h3 class="featured-paper__title"><a href="https://www.sciencedirect.com/science/article/pii/S0300908425002159?via%3Dihub">Decoding the genomic determinants of G-quadruplex stability: a comprehensive analysis of loop architecture and genomic context in the human genome</a></h3>
    <p class="featured-paper__venue"><strong>Biochimie</strong>, 2025</p>
    <div class="featured-paper__tags">
      <span>Human Genome</span>
      <span>G4 Stability</span>
      <span>Sequence Context</span>
    </div>
  </article>

  <article class="featured-paper">
    <div class="featured-paper__meta">Featured Resource • 2025</div>
    <h3 class="featured-paper__title"><a href="https://academic.oup.com/nar/article/53/D1/D1029/7848846">HSCGD: a comprehensive database of single-cell whole-genome data and metadata</a></h3>
    <p class="featured-paper__venue"><strong>Nucleic Acids Research</strong>, 2025</p>
    <div class="featured-paper__tags">
      <span>Single-Cell Genomics</span>
      <span>Database</span>
      <span>Metadata Resource</span>
    </div>
  </article>
</div>

### Full Publication List

<div class="publication-subsection">
  <h3>First-authored and Corresponding-authored</h3>
  {% include scholar_publication_list.html
    publications=site.data.google_scholar_publications.first_or_corresponding
    empty_message="First-authored or corresponding-authored publications will appear here after the Google Scholar data refresh." %}
</div>

<div class="publication-subsection">
  <h3>Co-authored</h3>
  {% include scholar_publication_list.html
    publications=site.data.google_scholar_publications.co_authored
    empty_message="Co-authored publications will appear here after the Google Scholar data refresh." %}
</div>
</div>

<div class="section-grid">
<div class="section-card section-card--compact section-card--awards" data-label="Recognition" markdown="1">
<span class='anchor' id='honors-and-awards'></span>
# 🎖 Honors and Awards
- National Encouragement Scholarship (2014, 2015)
</div>

<div class="section-card section-card--compact section-card--talks" data-label="Presentations" markdown="1">
<span class='anchor' id='invited-talks'></span>
# 💬 Invited Talks
- *2024.11*, "A comprehensive database of single-cell whole-genome data and metadata." National Doctoral Academic Forum on Biomedical Sensing and Detection, Taizhou, Zhejiang, China.
- *2023.11*, "Machine learning method for G-quadruplex detection based on nucleobase quality analysis from whole-genome resequencing data." GIW-ISCB Asia, Singapore.
</div>
</div>
