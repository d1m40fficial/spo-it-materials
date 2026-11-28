# Lesson explainers: series workflow

This is the workflow used for МДК.02.01. One Russian video per lecture, with a male voice,
burned-in captions, and a VK iframe on the site. Length is 60-180 seconds when the idea
needs room.

## One visual idea per lecture

There is no reusable final composition. Every lecture gets its own metaphor and the camera
moves through it. Reusing the same stations or cards with new labels is not enough.

- **Process models:** a route map. A waterfall staircase with a late return arrow, three
  short loops for iterations, a V with paired verification links, risk rings, and a
  compass for the choice.
- **Agile:** a yearly calendar collapses into a Scrum loop and a Kanban conveyor, then
  two lanes for product and support.
- **Requirements:** a vague phrase becomes a story card, then acceptance checks and a test.
- **Git:** snapshots, an index, a commit chain and branches.

Keep the shared look: paper background, Inter, the course accent, captions at the bottom.
Change the composition, not the brand.

## Voice and captions

Preferred male voice: `Voice: onecore:Pavel` (offline Windows) or
`Voice: edge:ru-RU-DmitryNeural` when the cloud endpoint accepts requests. Piper
`ru_RU-ruslan-medium` is the last resort; it puts stress on «тЕсты». Keep `Captions: on`:
`narrate.py` snaps Parakeet's words back to the script, so case endings stay correct.

## Build and QA

```
narrate.py <project>
render.py <project> --preview
render.py <project>
qa.py <project>
```

Require 10/10 checks and zero layout errors. Render 1920×1080; keep the master for VK.
Do not put masters under `courses/*/*/media/` root, because the site builder copies that
folder.

## VK and the site

Upload each master with the title `N. Lesson title`, e.g. `2. Модели процесса`, into the
subject playlist. The public page `https://vkvideo.ru/video-<oid>_<id>` becomes an iframe:

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

Rebuild the site, then commit and push. The builder renders a responsive iframe and does
not copy local video files.

## Handoff

Before upload, send the discipline once, then for every video the number, the title, and
the local path to the master. The person uploads to VK and returns the links; then the
iframes go into the chapters and the site is rebuilt and published.
