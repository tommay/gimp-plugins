#!/usr/bin/env python

# Save or export the current image -- do the right thing whether it's
# XCF (save) or any other format (export). This will mark the image clean,
# so GIMP won't warn you when you exit.
# Warning: this does not show a lot of extra dialogs, etc. or warn you
# if you're about to overwrite something! Use with caution.

# Copyright 2012 by Akkana Peck, http://www.shallowsky.com/software/
# You may use and distribute this plug-in under the terms of the GPL v2
# or, at your option, any later GPL version.

from gimpfu import *
import gtk
import os
import collections
import re

def python_export_clean(img, drawable) :
    chooser = gtk.FileChooserDialog(title=None,
                                    action=gtk.FILE_CHOOSER_ACTION_SAVE,
                                    buttons=(gtk.STOCK_SAVE_AS,
                                             gtk.RESPONSE_OK,
                                             gtk.STOCK_CANCEL,
                                             gtk.RESPONSE_CANCEL))

    filename = img.filename

    if not filename :
        # Might want to set a current folder:
        save_dir = choose_likely_save_dir()
        if save_dir :
            chooser.set_current_folder(save_dir)

        # Oh, cool, we could have shortcuts to image folders,
        # and maybe remove the stupid fstab shortcuts GTK adds for us.
        #chooser.add_shortcut_folder(folder)
        #chooser.remove_shortcut_folder(folder)
    else :
        # Create filenames for edited files the way I fo it manually:
        # IMG.JPG => IMB-a.JPG
        # IMG-a.JPG => IMG-b.JPG
        # IMG-a1.JPG => IMG-a2.JPG

        m = re.match(r"((.*-\w*)(.)|(.*))(\.\w+)", os.path.basename(filename))
        if m :
            chooser.set_current_folder(os.path.dirname(filename))
            if m.group(3) :
                filename = m.group(2) + chr(ord(m.group(3)) + 1) + m.group(5)
            else :
                filename = m.group(4) + "-a" + m.group(5)
            chooser.set_current_name(filename)
        else :
            chooser.set_filename(filename)

    chooser.set_do_overwrite_confirmation(True)

    response = chooser.run()
    if response != gtk.RESPONSE_OK:
        return

    filename = chooser.get_filename()
    img.filename = filename
    chooser.destroy()

    pdb.gimp_file_save(img, drawable, filename, filename)
    pdb.gimp_image_clean_all(img)

def choose_likely_save_dir() :
    counts = collections.Counter()
    for img in gimp.image_list() :
        if img.filename :
            counts[os.path.dirname(img.filename)] += 1
    
    try :
        return counts.most_common(1)[0][0]
    except :
        return None

register(
        "python_fu_export_clean",
        "Save or export the current image, then mark it clean.",
        "Save or export the current image, then mark it clean.",
        "Akkana Peck",
        "Akkana Peck",
        "2012",
        "Save/Export As + clean...",
        "*",
        [
            (PF_IMAGE, "image", "Input image", None),
            (PF_DRAWABLE, "drawable", "Input drawable", None),
        ],
        [],
        python_export_clean,
        menu = "<Image>/File/Save/"
)

main()

