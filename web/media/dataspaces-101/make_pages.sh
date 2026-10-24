#!/usr/bin/env bash
# Builds the player pages for the two Dataspaces 101 session recordings
# (24 Oct 2026), served from dresa.org.au/media/dataspaces-101/. Copied from
# the FAIR videos' builder: each page has a title, the browser's own video
# player (keyboard accessible), automatic captions (WebVTT), a description,
# the licence, and links on. Run in the folder holding the videos and captions.
set -e

page() {  # page <file stem> <title> <length> <description>
  local stem="$1" title="$2" length="$3" desc="$4"
  cat > "$stem.html" <<EOF
<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>$title | ARDC Dataspaces 101 recordings</title>
<style>
  :root { --navy: #0C223F; --teal: #00B0D5; }
  body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Arial, sans-serif; color: #222; background: #F4F8F7; line-height: 1.5; }
  header { background: var(--navy); color: #fff; padding: 20px 16px; }
  header a { color: #fff; }
  main { max-width: 960px; margin: 0 auto; padding: 20px 16px 40px; }
  h1 { margin: 0; font-size: 1.6rem; }
  video { width: 100%; height: auto; background: #000; border-radius: 8px; }
  .note { background: #fff; border-left: 4px solid var(--navy); padding: 8px 12px; font-size: 0.95rem; }
  a { color: #00597A; }
</style>
</head>
<body>
<header>
  <p style="margin:0 0 6px"><a href="./">ARDC Dataspaces 101 recordings</a></p>
  <h1>$title</h1>
</header>
<main>
  <video controls preload="metadata" playsinline>
    <source src="$stem.mp4" type="video/mp4">
    <track kind="captions" src="$stem.vtt" srclang="en" label="English (automatic)" default>
    Your browser cannot play this video. <a href="$stem.mp4">Download the video</a>.
  </video>
  <p class="note">$length. Captions were generated automatically and key terms corrected; they may contain errors.</p>
  <p>$desc</p>
  <p>Next: try the <a href="https://dresa.org.au/dataspaces_101/">Dataspaces 101 Coach</a>, ask the
     <a href="https://dresa.org.au/dataspaces_ed/">ARDC Dataspace Educator</a>, or read the
     <a href="https://ardc.edu.au/resource/australian-dataspaces-faqs/">Australian Dataspaces FAQs</a>.</p>
  <p style="font-size:0.9rem">Presented by Rob Clemens, Australian Research Data Commons (ARDC). Licence:
     <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
  <p><a href="https://dresa.org.au/educators">Back to DReSA Educators</a></p>
</main>
</body>
</html>
EOF
}

page dataspaces-101-session-1 "Dataspaces 101, Session 1: core concepts and the ideas that are easy to miss" "51 minutes, recorded 2026" \
  "An introduction to dataspaces in under an hour. Starts from a worked example (a foot-and-mouth disease outbreak near Darwin), gives a one-sentence definition and the four pillars (identity, trust, data sovereignty and interoperability), then focuses on the three ideas newcomers most often miss: rules before tools (the community-built rulebook comes before any technology), the control plane versus the data plane (and what a connector does), and trust as what you can prove, not just who you are. Closes with what it takes and roughly costs to build a dataspace in Australia, and where to read more: the DSSC Blueprint, the IDSA Rulebook, the Sitra rulebook and the IDS Reference Architecture Model."

page dataspaces-101-session-2 "Dataspaces 101, Session 2: reflections from early adopters and more key concepts" "1 hour 49 minutes, recorded July 2026" \
  "The follow-on session for a group who had completed Session 1. Reflects on what the participants took from it, demonstrates the Australian Dataspace Testbed (RMIT), clears up common misunderstandings (there is no central platform; the rulebook decides, the connector enforces), then goes deeper: the Dataspace Protocol (catalogues in DCAT, contract negotiation and transfer), how ODRL policies are enforced by a connector, federated learning, how a dataspace gets started (convene, business case, decision, governance and rulebook, onboarding, operations, proving value, scaling) and what a governance authority does. Includes a group exercise on a preventive biosecurity dataspace for foot-and-mouth disease and participants explaining dataspaces in their own words."

# Index page listing the recordings.
cat > index.html <<'EOF'
<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ARDC Dataspaces 101 recordings</title>
<style>
  body { margin: 0; font-family: system-ui, -apple-system, "Segoe UI", Arial, sans-serif; color: #222; background: #F4F8F7; line-height: 1.5; }
  header { background: #0C223F; color: #fff; padding: 20px 16px; }
  main { max-width: 960px; margin: 0 auto; padding: 20px 16px 40px; }
  h1 { margin: 0; font-size: 1.6rem; }
  a { color: #00597A; }
  li { margin: 8px 0; }
</style>
</head>
<body>
<header><h1>ARDC Dataspaces 101 recordings</h1></header>
<main>
  <p>Two recorded sessions from the ARDC introducing dataspaces: what they are, the ideas that are easy to miss, and how one gets started.</p>
  <ul>
    <li><a href="dataspaces-101-session-1.html">Session 1: core concepts and the ideas that are easy to miss</a> (51 minutes)</li>
    <li><a href="dataspaces-101-session-2.html">Session 2: reflections from early adopters and more key concepts</a> (1 hour 49 minutes)</li>
  </ul>
  <p>Both recordings have automatic captions. Presented by Rob Clemens, ARDC. Licence: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
  <p>Next: the <a href="https://dresa.org.au/dataspaces_101/">Dataspaces 101 Coach</a>, the
     <a href="https://dresa.org.au/dataspaces_ed/">ARDC Dataspace Educator</a> and the
     <a href="https://ardc.edu.au/resource/australian-dataspaces-faqs/">Australian Dataspaces FAQs</a>.</p>
  <p><a href="https://dresa.org.au/educators">Back to DReSA Educators</a></p>
</main>
</body>
</html>
EOF
echo "pages built"
