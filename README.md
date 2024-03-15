# StringArt

A project for a BWINF Wintercamp. (This fork was created from someone in this Camp)
the fork adds the ability to create rgb solutions

As seen in [this](https://youtube.com/watch?v=WGccIFf6MF8&feature=share8) video this project gives a framework to convert images to a series of threading operations that result in a (hopefully) beautiful artwork.

Also have a look at [this repo](https://github.com/bdring/StringArt/) where you can find different implementations as well as instructions how to actually build such a device.

Have a look at Aufgaben.md

![grafik](https://github.com/jon011235/StringArt/assets/148149771/337545ab-20e7-45b3-9d53-521fef0ed316)

![Uploading grafik.png…]()

## Requirements
For converting from img to threads you will need
```
pillow
numpy
```

For NixOS use: ```nix-shell -p python311Packages.pillow python311Packages.numpy``` (for python 3.11)
