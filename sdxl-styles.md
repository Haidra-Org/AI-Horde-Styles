Some of these duplicate the styles that I've added to the main styles fioe,
however some of those have m\been modified; whats in here is just the base
unmodified* styles as pulled from stable-diffusion-art.com/sdxl-styles and
processed with a "simple" regex)

The regex used to process the styles makes two changes:
  - replaces ` . ` with `, ` (more familiar)
  - replaces `{prompt}` with `{p}` (code reuse)

```
perl -0 -pe 's/\n\n/\\n/g;s/\n/ /g;s/\\n/\n\n/g;s/\s*([^\n]+)\n\nPrompt\n\n([^\n]+)\n\nNegative prompt\n\n([^\n]+)/    "\1": {\n      "prompt": "\2###\3",\n      "model": "SDXL_beta::stability.ai#6901",\n      "width": 1024,\n      "height": 1024\n      "steps": 50\n    },\n/g;s/\{prompt\}/{p}/g'
```

-----------------------------------------------------------

Format: I intend this file to be used as a supplementary prompt list of
uncurated styles that can be added to the main style list as required. As such,
it wraps the existing format with groups (separate from categories, the groups
are for sources. The main reason for this is the description/attribution).

Fair warning: if I make changes to this list in the future, I may decide to leqve out some parts. I'm also prone to typos. In other words: keep a fork and watch this repo if you're interested in using them

```
{
  "group name": {                 // the name of this key is the name of the group of styles that follows.
    "description": string,        // this is a description of the group, such as source, etc
    "description-md": string,     // Optional. description as markdown, if formatting required (used for links only currently)
    "description-html": string,   // Optional. description as html, if formatting required (used for links only currently)
    "styles": {                   // the syntax here matches the original styles.
      "name": {                     // name of the style
        "prompt": string,           // the prompt template. many of these are missing the {np}, as there was no indication of where to put it in the original source...
        "model": string,            // the model this style uses. Should perhaps be a category instead.
        "height": int,              // Although specified as defaults, height and width should be irrelevant; just make sure they're approximately 1048576 total pixels
        "width": int,               // see above. Unknown defaults for both height and width.
        "steps": int,               // steps are 50. can probably do slightly less. Unknown default
        "cfg": float,               // a multiple of 0.5 between (iirc) 0 and 30. check horde api to be sure, i'm too lazy rn. Unknown default
        "loras": [                  // Optional. sdxl doesn't currently support loras, but just in case 🤷. I explicitly want to allow use of inject_trigger:"all" and "inject_trigger": "any". Unknown default.
          {                          // up to 5 loras are allowed
            "name": "string"          // either the numeric id of the lora (for an ezact match) or the name (fuzzy search)
            "clip": float             // Optional. how much to apply the lora to the clip (text understanding) (I might be wrong, this may be inaccurate). defaults to 1
            "model": float            // Optional. how much to apply the lora to the unet (image generation) (I might be wrong, this may be inaccurate). default to 1
            "inject_trigger": string, // Optional. Specify a trigger to inject. Special cases: "all" injects *all* triggers fr\or the given lora into the prompt, while *any* injects a random trigger. Usual use: onject the trigger specified (why? just put it in the prompt!)
          }
        ]
      }
    }
  }
}
```

# Please enter the commit message for your changes. Lines starting
# with '#' will be ignored, and an empty message aborts the commit.
#
# Date:      Fri Aug 25 22:30:38 2023 -0700
#
# On branch main
# Your branch is ahead of 'origin/main' by 1 commit.
#   (use "git push" to publish your local commits)
#
# Changes to be committed:
#	new file:   sdxl-styles.json
#
# Untracked files:
#	bb
#	index.html
#	index.html.txt
#	n.js
#	styles.json.1
#
