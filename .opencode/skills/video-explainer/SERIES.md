# 4-scene lesson explainers

This is the series workflow used for МДК.02.01. It builds one 60-75 second Russian
video per lecture, with a male voice, burned-in captions, and a VK iframe on the site.

## Script

Four scenes, 120-150 spoken words total:

1. **Hook.** One concrete case: two projects, a broken archive, the phrase «сделайте
   удобно». Name the tension in the first three seconds.
2. **Mechanism.** Five steps, models, or artifacts on one line. This is the teachable core.
3. **Contrast.** Two numbers or two states side by side: early vs late feedback, a yearly
   plan vs a two-week sprint, «быстро» vs two seconds, an archive vs commits.
4. **Takeaway.** One sentence that answers the hook, then a stamp.

Set `Voice: edge:ru-RU-DmitryNeural`. If the Edge endpoint is rate-limited, use
`Voice: onecore:Pavel` (offline Windows male) or `Voice: piper:ru_RU-ruslan-medium`
(last resort: Ruslan puts stress on «тЕсты»). Keep `Captions: on`; `narrate.py` snaps
Parakeet's words back to the script, so case endings stay correct.

## Graphics

`assets/series-world.html` is the tokenized four-scene world. Replace tokens such as
`[[CASE_TITLE]]`, `[[ST1]]`, `[[ART1]]`, `[[LEFT_NUM]]`, `[[RIGHT_NUM]]`, `[[NOTE]]`,
`[[FINAL]]`, `[[STAMP1]]`, `[[STAMP4]]`, `[[LEFT_COLOR]]`, `[[RIGHT_COLOR]]`,
`[[BG2]]`, `[[BG3]]` and `[[ACCENT]]`. It gives:

- a case card with three symptoms and a red stamp;
- five stations with artifact chips above them;
- two big numbers with labels, a note, and early/late chips;
- a final line and a green stamp.

Choreography uses scene fractions, not word cues, so it survives small timing changes.
The camera drifts every scene; the left number fades before the pan to the right.

## Build and QA

```
narrate.py <project>
render.py <project> --preview
render.py <project>
qa.py <project>
```

Require 10/10 checks and zero layout errors. Keep the master 1920×1080 MP4 for VK; do
not put it under `courses/*/*/media/` root, because the site builder copies that folder.

## VK and the site

Upload each master with the title `N. Lesson title`, e.g. `2. Модели процесса`, into the
subject playlist. The public VK page URL `https://vkvideo.ru/video-<oid>_<id>` becomes an
iframe URL:

```
https://vkvideo.ru/video_ext.php?oid=-<oid>&id=<id>&hd=1
```

Insert it at the end of the lecture, before the quiz, with no visible caption:

```markdown
## Видеоразбор

One sentence about the video.

::video https://vkvideo.ru/video_ext.php?oid=-243783037&id=456239018&hd=1 | 2. Модели процесса

## Тест

::quiz
```

Rebuild the site, then commit and push. The site builder renders a responsive iframe and
does not copy local video files.

## Handoff

Before upload, send the discipline once, then for every video the number, the title, and
the local path to the master. The person uploads to VK and returns the links; then the
iframes go into the chapters and the site is rebuilt and published.
