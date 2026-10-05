#!/bin/zsh
# Desktop inteiro (160 quadros) e depois o mobile inteiro (100 quadros).
cd "${0:A:h}"
blender -b --factory-startup --python shot.py -- desktop "0-159" 32 "$PWD/renders/shot_desktop" 2>&1 | grep -E --line-buffered "SHOT_DONE|Traceback|Error"
FR=$(python3 -c "print(','.join(str(round(i*159/99)) for i in range(100)))")
rm -rf renders/shot_mobile
blender -b --factory-startup --python shot.py -- mobile "$FR" 32 "$PWD/renders/shot_mobile" 2>&1 | grep -E --line-buffered "SHOT_DONE|Traceback|Error"
echo ALL_DONE
