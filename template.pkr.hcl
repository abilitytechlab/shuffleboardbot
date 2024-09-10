source "arm-image" "raspberrypi" {
  iso_url              = "https://downloads.raspberrypi.org/raspios_lite_armhf_latest"
  iso_target_extension = "img"
  target_image_size    = "3G"
  image_type           = "raspberrypi"
  ssh_username         = "pi"
  ssh_password         = "raspberry"
  output_directory     = "output-images"
}

build {
  name    = "sjoel-pi-image"
  sources = ["source.arm-image.raspberrypi"]

  provisioner "file" {
    source      = "./install.sh"
    destination = "/tmp/install.sh"
  }

  provisioner "shell" {
    inline = [
      "chmod +x /tmp/install.sh",
      "sudo /tmp/install.sh",
    ]
  }
}
