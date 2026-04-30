# Design: Transitions, Grid, and Animations

Schema entries for three CSS property groups: Transitions (5 properties), Grid (15 properties), and Animations (12 properties).

---

## New Unit Types Required (units.json)

### Time
CSS time values for durations and delays. No existing `Time` unit found in units.json.

```json
"Time": {
    "cases": {
        "s": {
            "values": ["Double"],
            "names": ["value"],
            "description": "Defines a time in seconds.",
            "format": "{{value}}s"
        },
        "ms": {
            "values": ["Int"],
            "names": ["value"],
            "description": "Defines a time in milliseconds.",
            "format": "{{value}}ms"
        }
    },
    "description": "A time value."
}
```

### TimingFunction
CSS easing functions for transitions and animations.

```json
"TimingFunction": {
    "cases": {
        "ease": {
            "description": "Default easing — slow start, fast middle, slow end."
        },
        "ease-in": {
            "description": "Slow start."
        },
        "ease-out": {
            "description": "Slow end."
        },
        "ease-in-out": {
            "description": "Slow start and end."
        },
        "linear": {
            "description": "Constant speed throughout."
        },
        "step-start": {
            "description": "Equivalent to steps(1, jump-start)."
        },
        "step-end": {
            "description": "Equivalent to steps(1, jump-end)."
        },
        "cubic-bezier": {
            "values": ["Double", "Double", "Double", "Double"],
            "names": ["x1", "y1", "x2", "y2"],
            "description": "Custom cubic bezier curve.",
            "format": "cubic-bezier({{x1}}, {{y1}}, {{x2}}, {{y2}})"
        },
        "steps:0": {
            "values": ["Int"],
            "names": ["count"],
            "description": "Steps function with count only.",
            "format": "steps({{count}})"
        },
        "steps:1": {
            "values": ["Int", "Unit.StepPosition"],
            "names": ["count", "position"],
            "description": "Steps function with count and position.",
            "format": "steps({{count}}, {{position}})"
        }
    },
    "description": "A timing function for transitions and animations."
}
```

### StepPosition
Helper enum for `steps()` timing function.

```json
"StepPosition": {
    "cases": {
        "jump-start": {
            "description": "The first rise happens at input progress 0."
        },
        "jump-end": {
            "description": "The last rise happens at input progress 1."
        },
        "jump-none": {
            "description": "No jump at start or end."
        },
        "jump-both": {
            "description": "Jumps at both start and end."
        },
        "start": {
            "description": "Equivalent to jump-start."
        },
        "end": {
            "description": "Equivalent to jump-end."
        }
    },
    "description": "The position of steps in a step timing function."
}
```

### TransitionProperty
Which CSS property to transition.

```json
"TransitionProperty": {
    "cases": {
        "none": {
            "description": "No property will transition."
        },
        "all": {
            "description": "All properties will transition."
        },
        "custom": {
            "values": ["String"],
            "names": ["property"],
            "description": "A specific CSS property to transition.",
            "format": "{{property}}"
        }
    },
    "description": "The CSS property to apply a transition to."
}
```

### GridAutoFlow

```json
"GridAutoFlow": {
    "cases": {
        "row": {
            "description": "Items are placed by filling each row."
        },
        "column": {
            "description": "Items are placed by filling each column."
        },
        "dense": {
            "description": "Packing algorithm attempts to fill holes."
        },
        "row-dense": {
            "description": "Items fill rows using dense packing.",
            "format": "row dense"
        },
        "column-dense": {
            "description": "Items fill columns using dense packing.",
            "format": "column dense"
        }
    },
    "description": "How auto-placed items flow into the grid."
}
```

### GridTrackSize
Used for grid-template-columns, grid-template-rows, grid-auto-columns, grid-auto-rows.

```json
"GridTrackSize": {
    "inherit": ["Length", "Percentage"],
    "cases": {
        "auto": {
            "description": "The track is sized automatically."
        },
        "min-content": {
            "description": "The track is sized to the minimum content."
        },
        "max-content": {
            "description": "The track is sized to the maximum content."
        },
        "fr": {
            "values": ["Double"],
            "names": ["value"],
            "description": "A fractional unit of remaining space.",
            "format": "{{value}}fr"
        },
        "minmax": {
            "values": ["Unit.GridTrackMin", "Unit.GridTrackMax"],
            "names": ["min", "max"],
            "description": "A size range between min and max.",
            "format": "minmax({{min}}, {{max}})"
        },
        "fit-content": {
            "values": ["Unit.LengthPercentage"],
            "names": ["value"],
            "description": "Clamps to fit-content formula.",
            "format": "fit-content({{value}})"
        },
        "repeat:0": {
            "values": ["Int", "Unit.GridTrackList"],
            "names": ["count", "tracks"],
            "description": "Repeats a track pattern a fixed number of times.",
            "format": "repeat({{count}}, {{tracks}})"
        },
        "repeat:1": {
            "values": ["Unit.AutoRepeat", "Unit.GridTrackList"],
            "names": ["auto", "tracks"],
            "description": "Repeats a track pattern with auto-fill or auto-fit.",
            "format": "repeat({{auto}}, {{tracks}})"
        }
    },
    "description": "The sizing of a grid track."
}
```

### GridTrackMin
Minimum bound for minmax().

```json
"GridTrackMin": {
    "inherit": ["Length", "Percentage"],
    "cases": {
        "auto": {
            "description": "Automatic minimum."
        },
        "min-content": {
            "description": "The minimum content size."
        },
        "max-content": {
            "description": "The maximum content size."
        },
        "fr": {
            "values": ["Double"],
            "names": ["value"],
            "description": "A fractional unit.",
            "format": "{{value}}fr"
        }
    },
    "description": "The minimum bound of a grid track."
}
```

### GridTrackMax
Maximum bound for minmax().

```json
"GridTrackMax": {
    "inherit": ["Length", "Percentage"],
    "cases": {
        "auto": {
            "description": "Automatic maximum."
        },
        "min-content": {
            "description": "The minimum content size."
        },
        "max-content": {
            "description": "The maximum content size."
        },
        "fr": {
            "values": ["Double"],
            "names": ["value"],
            "description": "A fractional unit.",
            "format": "{{value}}fr"
        }
    },
    "description": "The maximum bound of a grid track."
}
```

### GridTrackList
A sequence of track sizes for repeat() and template definitions.

```json
"GridTrackList": {
    "cases": {
        "tracks": {
            "values": ["sequence[Unit.GridTrackSize]"],
            "names": ["sizes"],
            "description": "A list of track sizes.",
            "format": "#SEQ "
        }
    },
    "description": "A list of grid track sizes."
}
```

### AutoRepeat

```json
"AutoRepeat": {
    "cases": {
        "auto-fill": {
            "description": "Fill with as many tracks as fit."
        },
        "auto-fit": {
            "description": "Fill and collapse empty tracks."
        }
    },
    "description": "Auto repeat mode for grid tracks."
}
```

### GridTemplateAreas

```json
"GridTemplateAreas": {
    "cases": {
        "none": {
            "description": "No named grid areas."
        },
        "areas": {
            "values": ["sequence[String]"],
            "names": ["rows"],
            "description": "Named grid areas as quoted row strings.",
            "format": "#SEQ "
        }
    },
    "description": "Named grid template areas."
}
```

### AnimationDirection

```json
"AnimationDirection": {
    "cases": {
        "normal": {
            "description": "The animation plays forwards."
        },
        "reverse": {
            "description": "The animation plays backwards."
        },
        "alternate": {
            "description": "The animation alternates between forwards and backwards."
        },
        "alternate-reverse": {
            "description": "The animation alternates starting backwards."
        }
    },
    "description": "The direction of an animation."
}
```

### AnimationFillMode

```json
"AnimationFillMode": {
    "cases": {
        "none": {
            "description": "No fill mode applied."
        },
        "forwards": {
            "description": "Retains the last keyframe styles."
        },
        "backwards": {
            "description": "Applies the first keyframe styles before start."
        },
        "both": {
            "description": "Applies both forwards and backwards fill."
        }
    },
    "description": "How styles apply before and after animation."
}
```

### AnimationIterationCount

```json
"AnimationIterationCount": {
    "cases": {
        "infinite": {
            "description": "The animation repeats indefinitely."
        },
        "count": {
            "values": ["Double"],
            "names": ["value"],
            "description": "The animation repeats a specific number of times.",
            "format": "{{value}}"
        }
    },
    "description": "How many times the animation repeats."
}
```

### AnimationName

```json
"AnimationName": {
    "cases": {
        "none": {
            "description": "No animation."
        },
        "custom": {
            "values": ["String"],
            "names": ["name"],
            "description": "A named keyframes animation.",
            "format": "{{name}}"
        }
    },
    "description": "The name of a keyframes animation."
}
```

### AnimationPlayState

```json
"AnimationPlayState": {
    "cases": {
        "running": {
            "description": "The animation is playing."
        },
        "paused": {
            "description": "The animation is paused."
        }
    },
    "description": "Whether the animation is running or paused."
}
```

### TransformFunction
Individual transform functions for the `transform` property.

```json
"TransformFunction": {
    "cases": {
        "none": {
            "description": "No transform."
        },
        "translate:0": {
            "values": ["Unit.LengthPercentage"],
            "names": ["x"],
            "description": "Translate in the x-axis.",
            "format": "translate({{x}})"
        },
        "translate:1": {
            "values": ["Unit.LengthPercentage", "Unit.LengthPercentage"],
            "names": ["x", "y"],
            "description": "Translate in x and y axes.",
            "format": "translate({{x}}, {{y}})"
        },
        "translateX": {
            "values": ["Unit.LengthPercentage"],
            "names": ["x"],
            "description": "Translate in the x-axis.",
            "format": "translateX({{x}})"
        },
        "translateY": {
            "values": ["Unit.LengthPercentage"],
            "names": ["y"],
            "description": "Translate in the y-axis.",
            "format": "translateY({{y}})"
        },
        "translateZ": {
            "values": ["Unit.Length"],
            "names": ["z"],
            "description": "Translate in the z-axis.",
            "format": "translateZ({{z}})"
        },
        "translate3d": {
            "values": ["Unit.LengthPercentage", "Unit.LengthPercentage", "Unit.Length"],
            "names": ["x", "y", "z"],
            "description": "Translate in all three axes.",
            "format": "translate3d({{x}}, {{y}}, {{z}})"
        },
        "scale:0": {
            "values": ["Double"],
            "names": ["xy"],
            "description": "Scale uniformly.",
            "format": "scale({{xy}})"
        },
        "scale:1": {
            "values": ["Double", "Double"],
            "names": ["x", "y"],
            "description": "Scale in x and y axes.",
            "format": "scale({{x}}, {{y}})"
        },
        "scaleX": {
            "values": ["Double"],
            "names": ["x"],
            "description": "Scale in the x-axis.",
            "format": "scaleX({{x}})"
        },
        "scaleY": {
            "values": ["Double"],
            "names": ["y"],
            "description": "Scale in the y-axis.",
            "format": "scaleY({{y}})"
        },
        "scaleZ": {
            "values": ["Double"],
            "names": ["z"],
            "description": "Scale in the z-axis.",
            "format": "scaleZ({{z}})"
        },
        "scale3d": {
            "values": ["Double", "Double", "Double"],
            "names": ["x", "y", "z"],
            "description": "Scale in all three axes.",
            "format": "scale3d({{x}}, {{y}}, {{z}})"
        },
        "rotate:0": {
            "values": ["Unit.Angle"],
            "names": ["angle"],
            "description": "Rotate by an angle.",
            "format": "rotate({{angle}})"
        },
        "rotateX": {
            "values": ["Unit.Angle"],
            "names": ["angle"],
            "description": "Rotate around the x-axis.",
            "format": "rotateX({{angle}})"
        },
        "rotateY": {
            "values": ["Unit.Angle"],
            "names": ["angle"],
            "description": "Rotate around the y-axis.",
            "format": "rotateY({{angle}})"
        },
        "rotateZ": {
            "values": ["Unit.Angle"],
            "names": ["angle"],
            "description": "Rotate around the z-axis.",
            "format": "rotateZ({{angle}})"
        },
        "rotate3d": {
            "values": ["Double", "Double", "Double", "Unit.Angle"],
            "names": ["x", "y", "z", "angle"],
            "description": "Rotate around a vector axis.",
            "format": "rotate3d({{x}}, {{y}}, {{z}}, {{angle}})"
        },
        "skew:0": {
            "values": ["Unit.Angle"],
            "names": ["x"],
            "description": "Skew in the x-axis.",
            "format": "skew({{x}})"
        },
        "skew:1": {
            "values": ["Unit.Angle", "Unit.Angle"],
            "names": ["x", "y"],
            "description": "Skew in x and y axes.",
            "format": "skew({{x}}, {{y}})"
        },
        "skewX": {
            "values": ["Unit.Angle"],
            "names": ["x"],
            "description": "Skew in the x-axis.",
            "format": "skewX({{x}})"
        },
        "skewY": {
            "values": ["Unit.Angle"],
            "names": ["y"],
            "description": "Skew in the y-axis.",
            "format": "skewY({{y}})"
        },
        "matrix": {
            "values": ["Double", "Double", "Double", "Double", "Double", "Double"],
            "names": ["a", "b", "c", "d", "tx", "ty"],
            "description": "2D transformation matrix.",
            "format": "matrix({{a}}, {{b}}, {{c}}, {{d}}, {{tx}}, {{ty}})"
        },
        "matrix3d": {
            "values": ["Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double", "Double"],
            "names": ["a1", "b1", "c1", "d1", "a2", "b2", "c2", "d2", "a3", "b3", "c3", "d3", "a4", "b4", "c4", "d4"],
            "description": "3D transformation matrix.",
            "format": "matrix3d({{a1}}, {{b1}}, {{c1}}, {{d1}}, {{a2}}, {{b2}}, {{c2}}, {{d2}}, {{a3}}, {{b3}}, {{c3}}, {{d3}}, {{a4}}, {{b4}}, {{c4}}, {{d4}})"
        },
        "perspective": {
            "values": ["Unit.Length"],
            "names": ["depth"],
            "description": "Applies perspective transform.",
            "format": "perspective({{depth}})"
        }
    },
    "description": "Individual CSS transform functions."
}
```

### TransformBox

```json
"TransformBox": {
    "cases": {
        "content-box": {
            "description": "The content box is the reference box."
        },
        "border-box": {
            "description": "The border box is the reference box."
        },
        "fill-box": {
            "description": "The object bounding box is the reference box."
        },
        "stroke-box": {
            "description": "The stroke bounding box is the reference box."
        },
        "view-box": {
            "description": "The SVG viewport is the reference box."
        }
    },
    "description": "The reference box for transform and transform-origin."
}
```

### TransformOriginXY
Reuses existing PositionX / PositionY but with Length fallback. Already have `ObjectPosition` which works.

No new type needed — reuse existing `Unit.ObjectPosition` for transform-origin (it supports `x y` and positional keywords the same way CSS transform-origin does).

---

## Properties (properties.json)

### 1. Transitions (5 properties)

```json
"transition:0": {
    "shorthand": true,
    "description": "Sets the transition shorthand property.",
    "types": ["Unit.TransitionProperty", "Unit.Time", "Unit.TimingFunction", "Unit.Time"],
    "names": ["property", "duration", "timingFunction", "delay"],
    "format": "{{property}} {{duration}} {{timingFunction}} {{delay}}"
},
"transition:1": {
    "shorthand": true,
    "description": "Sets the transition shorthand property.",
    "types": ["Unit.TransitionProperty", "Unit.Time", "Unit.TimingFunction"],
    "names": ["property", "duration", "timingFunction"],
    "format": "{{property}} {{duration}} {{timingFunction}}"
},
"transition:2": {
    "shorthand": true,
    "description": "Sets the transition shorthand property.",
    "types": ["Unit.TransitionProperty", "Unit.Time"],
    "names": ["property", "duration"],
    "format": "{{property}} {{duration}}"
},
"transition-*": {
    "delay": {
        "description": "Sets the transition delay property.",
        "types": ["Unit.Time"],
        "names": ["delay"],
        "format": "{{delay}}"
    },
    "duration": {
        "description": "Sets the transition duration property.",
        "types": ["Unit.Time"],
        "names": ["duration"],
        "format": "{{duration}}"
    },
    "property:0": {
        "description": "Sets the transition property property.",
        "types": ["Unit.TransitionProperty"],
        "names": ["property"],
        "format": "{{property}}"
    },
    "property:1": {
        "description": "Sets the transition property to a list of properties.",
        "types": ["sequence[Unit.TransitionProperty]"],
        "names": ["properties"],
        "format": "#SEQ,"
    },
    "timing-function": {
        "description": "Sets the transition timing function property.",
        "types": ["Unit.TimingFunction"],
        "names": ["timingFunction"],
        "format": "{{timingFunction}}"
    }
}
```

### 2. Grid (15 properties)

Existing entry to **replace** (currently only has `area:0`):

```json
"grid-*": {
    "area:0": {
        "description": "Sets the grid area property.",
        "types": ["Unit.GridLine"],
        "names": ["area"],
        "format": "{{area}}"
    },
    "area:1": {
        "description": "Sets the grid area property with row and column.",
        "types": ["Unit.GridLine", "Unit.GridLine"],
        "names": ["rowStart", "columnStart"],
        "format": "{{rowStart}} / {{columnStart}}"
    },
    "area:2": {
        "description": "Sets the grid area property with row start/end and column start.",
        "types": ["Unit.GridLine", "Unit.GridLine", "Unit.GridLine"],
        "names": ["rowStart", "columnStart", "rowEnd"],
        "format": "{{rowStart}} / {{columnStart}} / {{rowEnd}}"
    },
    "area:3": {
        "description": "Sets the grid area property with all four values.",
        "types": ["Unit.GridLine", "Unit.GridLine", "Unit.GridLine", "Unit.GridLine"],
        "names": ["rowStart", "columnStart", "rowEnd", "columnEnd"],
        "format": "{{rowStart}} / {{columnStart}} / {{rowEnd}} / {{columnEnd}}"
    },
    "auto-columns:0": {
        "description": "Sets the grid auto columns property.",
        "types": ["Unit.GridTrackSize"],
        "names": ["size"],
        "format": "{{size}}"
    },
    "auto-columns:1": {
        "description": "Sets the grid auto columns property with multiple track sizes.",
        "types": ["sequence[Unit.GridTrackSize]"],
        "names": ["sizes"],
        "format": "#SEQ "
    },
    "auto-flow": {
        "description": "Sets the grid auto flow property.",
        "types": ["Unit.GridAutoFlow"],
        "names": ["flow"],
        "format": "{{flow}}"
    },
    "auto-rows:0": {
        "description": "Sets the grid auto rows property.",
        "types": ["Unit.GridTrackSize"],
        "names": ["size"],
        "format": "{{size}}"
    },
    "auto-rows:1": {
        "description": "Sets the grid auto rows property with multiple track sizes.",
        "types": ["sequence[Unit.GridTrackSize]"],
        "names": ["sizes"],
        "format": "#SEQ "
    },
    "column:0": {
        "description": "Sets the grid column property.",
        "types": ["Unit.GridLine"],
        "names": ["start"],
        "format": "{{start}}"
    },
    "column:1": {
        "description": "Sets the grid column start and end.",
        "types": ["Unit.GridLine", "Unit.GridLine"],
        "names": ["start", "end"],
        "format": "{{start}} / {{end}}"
    },
    "column-end": {
        "description": "Sets the grid column end property.",
        "types": ["Unit.GridLine"],
        "names": ["end"],
        "format": "{{end}}"
    },
    "column-start": {
        "description": "Sets the grid column start property.",
        "types": ["Unit.GridLine"],
        "names": ["start"],
        "format": "{{start}}"
    },
    "gap:0": {
        "description": "Sets the grid gap property (same as gap).",
        "shorthand": true,
        "types": ["Unit.LengthPercentage"],
        "names": ["both"],
        "format": "{{both}}"
    },
    "gap:1": {
        "description": "Sets the grid gap property with row and column.",
        "shorthand": true,
        "types": ["Unit.LengthPercentage", "Unit.LengthPercentage"],
        "names": ["row", "column"],
        "format": "{{row}} {{column}}"
    },
    "row:0": {
        "description": "Sets the grid row property.",
        "types": ["Unit.GridLine"],
        "names": ["start"],
        "format": "{{start}}"
    },
    "row:1": {
        "description": "Sets the grid row start and end.",
        "types": ["Unit.GridLine", "Unit.GridLine"],
        "names": ["start", "end"],
        "format": "{{start}} / {{end}}"
    },
    "row-end": {
        "description": "Sets the grid row end property.",
        "types": ["Unit.GridLine"],
        "names": ["end"],
        "format": "{{end}}"
    },
    "row-start": {
        "description": "Sets the grid row start property.",
        "types": ["Unit.GridLine"],
        "names": ["start"],
        "format": "{{start}}"
    },
    "template-areas": {
        "description": "Sets the grid template areas property.",
        "types": ["Unit.GridTemplateAreas"],
        "names": ["areas"],
        "format": "{{areas}}"
    },
    "template-columns:0": {
        "description": "Sets the grid template columns property.",
        "types": ["Unit.GridTrackSize"],
        "names": ["size"],
        "format": "{{size}}"
    },
    "template-columns:1": {
        "description": "Sets the grid template columns property with multiple tracks.",
        "types": ["sequence[Unit.GridTrackSize]"],
        "names": ["sizes"],
        "format": "#SEQ "
    },
    "template-rows:0": {
        "description": "Sets the grid template rows property.",
        "types": ["Unit.GridTrackSize"],
        "names": ["size"],
        "format": "{{size}}"
    },
    "template-rows:1": {
        "description": "Sets the grid template rows property with multiple tracks.",
        "types": ["sequence[Unit.GridTrackSize]"],
        "names": ["sizes"],
        "format": "#SEQ "
    }
}
```

Top-level `grid` shorthand (extremely complex in CSS, provide practical overloads):

```json
"grid:0": {
    "shorthand": true,
    "description": "Sets the grid shorthand with template rows and columns.",
    "types": ["sequence[Unit.GridTrackSize]", "sequence[Unit.GridTrackSize]"],
    "names": ["templateRows", "templateColumns"],
    "format": "#SEQ  / #SEQ "
},
"grid:1": {
    "shorthand": true,
    "description": "Sets the grid shorthand with auto-flow rows.",
    "types": ["Unit.GridAutoFlow", "sequence[Unit.GridTrackSize]"],
    "names": ["autoFlow", "autoColumns"],
    "format": "{{autoFlow}} / #SEQ "
},
"grid:2": {
    "shorthand": true,
    "description": "Sets the grid to none.",
    "types": ["Unit.None"],
    "names": ["none"],
    "format": "{{none}}"
}
```

### 3. Animations (12 properties)

```json
"animation:0": {
    "shorthand": true,
    "description": "Sets the animation shorthand property.",
    "types": ["Unit.AnimationName", "Unit.Time", "Unit.TimingFunction", "Unit.Time", "Unit.AnimationIterationCount", "Unit.AnimationDirection", "Unit.AnimationFillMode", "Unit.AnimationPlayState"],
    "names": ["name", "duration", "timingFunction", "delay", "iterationCount", "direction", "fillMode", "playState"],
    "format": "{{name}} {{duration}} {{timingFunction}} {{delay}} {{iterationCount}} {{direction}} {{fillMode}} {{playState}}"
},
"animation:1": {
    "shorthand": true,
    "description": "Sets the animation shorthand with name, duration, and timing.",
    "types": ["Unit.AnimationName", "Unit.Time", "Unit.TimingFunction"],
    "names": ["name", "duration", "timingFunction"],
    "format": "{{name}} {{duration}} {{timingFunction}}"
},
"animation:2": {
    "shorthand": true,
    "description": "Sets the animation shorthand with name and duration.",
    "types": ["Unit.AnimationName", "Unit.Time"],
    "names": ["name", "duration"],
    "format": "{{name}} {{duration}}"
},
"animation-*": {
    "delay": {
        "description": "Sets the animation delay property.",
        "types": ["Unit.Time"],
        "names": ["delay"],
        "format": "{{delay}}"
    },
    "direction": {
        "description": "Sets the animation direction property.",
        "types": ["Unit.AnimationDirection"],
        "names": ["direction"],
        "format": "{{direction}}"
    },
    "duration": {
        "description": "Sets the animation duration property.",
        "types": ["Unit.Time"],
        "names": ["duration"],
        "format": "{{duration}}"
    },
    "fill-mode": {
        "description": "Sets the animation fill mode property.",
        "types": ["Unit.AnimationFillMode"],
        "names": ["fillMode"],
        "format": "{{fillMode}}"
    },
    "iteration-count": {
        "description": "Sets the animation iteration count property.",
        "types": ["Unit.AnimationIterationCount"],
        "names": ["count"],
        "format": "{{count}}"
    },
    "name": {
        "description": "Sets the animation name property.",
        "types": ["Unit.AnimationName"],
        "names": ["name"],
        "format": "{{name}}"
    },
    "play-state": {
        "description": "Sets the animation play state property.",
        "types": ["Unit.AnimationPlayState"],
        "names": ["playState"],
        "format": "{{playState}}"
    },
    "timing-function": {
        "description": "Sets the animation timing function property.",
        "types": ["Unit.TimingFunction"],
        "names": ["timingFunction"],
        "format": "{{timingFunction}}"
    }
},
"transform:0": {
    "description": "Sets the transform property with a single function.",
    "types": ["Unit.TransformFunction"],
    "names": ["transform"],
    "format": "{{transform}}"
},
"transform:1": {
    "description": "Sets the transform property with multiple functions.",
    "types": ["sequence[Unit.TransformFunction]"],
    "names": ["transforms"],
    "format": "#SEQ "
},
"transform-*": {
    "box": {
        "description": "Sets the transform box property.",
        "types": ["Unit.TransformBox"],
        "names": ["box"],
        "format": "{{box}}"
    },
    "origin:0": {
        "description": "Sets the transform origin with a single value.",
        "types": ["Unit.LengthPercentage"],
        "names": ["offset"],
        "format": "{{offset}}"
    },
    "origin:1": {
        "description": "Sets the transform origin with x and y.",
        "types": ["Unit.LengthPercentage", "Unit.LengthPercentage"],
        "names": ["x", "y"],
        "format": "{{x}} {{y}}"
    },
    "origin:2": {
        "description": "Sets the transform origin with x, y, and z.",
        "types": ["Unit.LengthPercentage", "Unit.LengthPercentage", "Unit.Length"],
        "names": ["x", "y", "z"],
        "format": "{{x}} {{y}} {{z}}"
    },
    "origin:3": {
        "description": "Sets the transform origin with keyword positions.",
        "types": ["Unit.ObjectPosition"],
        "names": ["position"],
        "format": "{{position}}"
    }
}
```

---

## Summary of New Unit Types

| Unit Type | Purpose |
|---|---|
| `Time` | seconds, milliseconds for durations/delays |
| `TimingFunction` | ease, linear, cubic-bezier, steps |
| `StepPosition` | jump-start, jump-end, etc. for steps() |
| `TransitionProperty` | none, all, or custom property name |
| `GridAutoFlow` | row, column, dense, row-dense, column-dense |
| `GridTrackSize` | auto, fr, minmax, fit-content, repeat, lengths |
| `GridTrackMin` | minimum bound for minmax() |
| `GridTrackMax` | maximum bound for minmax() |
| `GridTrackList` | sequence of track sizes |
| `AutoRepeat` | auto-fill, auto-fit |
| `GridTemplateAreas` | none or quoted row strings |
| `AnimationDirection` | normal, reverse, alternate, alternate-reverse |
| `AnimationFillMode` | none, forwards, backwards, both |
| `AnimationIterationCount` | infinite or numeric count |
| `AnimationName` | none or custom keyframe name |
| `AnimationPlayState` | running, paused |
| `TransformFunction` | translate, scale, rotate, skew, matrix, perspective |
| `TransformBox` | content-box, border-box, fill-box, stroke-box, view-box |

## Existing Unit Types Reused

| Unit Type | Used For |
|---|---|
| `GridLine` | grid-column-start/end, grid-row-start/end, grid-area |
| `Angle` | rotate transforms |
| `Length` | translate z, perspective |
| `LengthPercentage` | translate x/y, transform-origin, grid tracks |
| `ObjectPosition` | transform-origin keyword variant |
| `None` | grid:2 shorthand |
| `NoneLength` | already used for perspective property |

## Properties Coverage

| Group | Properties Covered | Count |
|---|---|---|
| **Transitions** | transition, transition-delay, transition-duration, transition-property, transition-timing-function | 5 |
| **Grid** | grid, grid-area, grid-auto-columns, grid-auto-flow, grid-auto-rows, grid-column, grid-column-end, grid-column-start, grid-gap, grid-row, grid-row-end, grid-row-start, grid-template-areas, grid-template-columns, grid-template-rows | 15 |
| **Animations** | animation, animation-delay, animation-direction, animation-duration, animation-fill-mode, animation-iteration-count, animation-name, animation-play-state, animation-timing-function, transform, transform-box, transform-origin | 12 |
| **Total** | | **32** |
