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
- *2025.05.07*: &nbsp;Successfully passed the Ph.D. defense. I am deeply grateful to Prof. [Zuhong Lu](https://scholar.google.com/scholar?q=author%3A%22Zuhong+Lu%22) and Prof. [Jing Tu](https://scholar.google.com/scholar?q=author%3A%22Jing+Tu%22) for their guidance as my supervisors, to Prof. [Xiaowo Wang](https://scholar.google.com/scholar?q=author%3A%22Xiaowo+Wang%22) for serving as the defense chair, and to all my lab partners for their support. 🎆
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

{% include featured_publication_cards.html publications=site.data.google_scholar_publications.featured_publications %}

### Full Publication List

<p class="publication-role-note">Co-first authors are indicated by <strong>†</strong>, and corresponding authors are indicated by <strong>*</strong>.</p>

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
