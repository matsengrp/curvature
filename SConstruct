import glob
import os

VariantDir('_build', src_dir='.')

env = Environment(ENV=os.environ)
inkscape_pdf = Builder(
    action = 'inkscape --without-gui --export-area-drawing --export-pdf=$TARGET $SOURCE')
inkscape_png = Builder(
    action = 'inkscape --without-gui --export-area-drawing --export-dpi 300 --export-png=$TARGET $SOURCE')

env['BUILDERS']['InkscapePng'] = inkscape_png
env['BUILDERS']['Latexdiff'] = Builder(action = 'latexdiff $SOURCES > $TARGET')
env['BUILDERS']['Copier'] = Builder(action = Copy('$TARGET', '$SOURCE'))

figure_pngs = [env.InkscapePng(target="figs/" + os.path.basename(svg).replace('.svg','.png'), source=svg)
               for svg in glob.glob('prefigs/*.svg')]

pdfs = [env.Copier(target = '_build/' + os.path.basename(pdf), source = pdf)
        for pdf in glob.glob('figures/*.pdf')]

#Depends(Flatten([pdfs]), Flatten([figure_pngs]))

curvature=env.PDF(target='_build/curvature.pdf',source='curvature.tex')

Depends(Flatten([curvature]),
        Flatten([pdfs, 'curvature.bib']))

cont_build = env.Command('.continuous', ['curvature.bib', 'curvature.tex'],
    'while :; do inotifywait -e modify $SOURCES; scons -Q; done')
Alias('continuous', cont_build)

Default(curvature)
