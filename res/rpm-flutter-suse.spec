Name:       rustdesk-sut
Version:    1.4.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://github.com/shirh19910112/rustdesk-sut
Vendor:     RustDesk-SUT
Requires:   gtk3 libxcb1 libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1 xdotool
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/rustdesk-sut" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/rustdesk-sut"
mv "%{buildroot}/usr/share/rustdesk-sut/rustdesk" "%{buildroot}/usr/share/rustdesk-sut/rustdesk-sut"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/rustdesk.service "%{buildroot}/usr/share/rustdesk-sut/files/rustdesk-sut.service"
install -Dm 644 $HBB/res/rustdesk.desktop "%{buildroot}/usr/share/rustdesk-sut/files/rustdesk-sut.desktop"
install -Dm 644 $HBB/res/rustdesk-link.desktop "%{buildroot}/usr/share/rustdesk-sut/files/rustdesk-sut-link.desktop"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/rustdesk-sut.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/rustdesk-sut.svg"

%files
/usr/share/rustdesk-sut/*
/usr/share/rustdesk-sut/files/rustdesk-sut.service
/usr/share/icons/hicolor/256x256/apps/rustdesk-sut.png
/usr/share/icons/hicolor/scalable/apps/rustdesk-sut.svg
/usr/share/rustdesk-sut/files/rustdesk-sut.desktop
/usr/share/rustdesk-sut/files/rustdesk-sut-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop rustdesk-sut || true
  ;;
esac

%post
cp /usr/share/rustdesk-sut/files/rustdesk-sut.service /etc/systemd/system/rustdesk-sut.service
cp /usr/share/rustdesk-sut/files/rustdesk-sut.desktop /usr/share/applications/
cp /usr/share/rustdesk-sut/files/rustdesk-sut-link.desktop /usr/share/applications/
ln -sf /usr/share/rustdesk-sut/rustdesk-sut /usr/bin/rustdesk-sut
systemctl daemon-reload
systemctl enable rustdesk-sut
systemctl start rustdesk-sut
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop rustdesk-sut || true
    systemctl disable rustdesk-sut || true
    rm /etc/systemd/system/rustdesk-sut.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/rustdesk-sut || true
    rmdir /usr/lib/rustdesk-sut || true
    rmdir /usr/local/rustdesk-sut || true
    rmdir /usr/share/rustdesk-sut || true
    rm /usr/share/applications/rustdesk-sut.desktop || true
    rm /usr/share/applications/rustdesk-sut-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/rustdesk-sut || true
    rmdir /usr/local/rustdesk-sut || true
  ;;
esac
