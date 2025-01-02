# NTP server list from: RITM0096493 RITM1289210
%define ntpservers nsntp1.fnal.gov nsntp2.fnal.gov nsntp3.fnal.gov nsntp4.fnal.gov nsntp5.fnal.gov

Name:		fermilab-conf_timesync
Version:	1.0
Release:	7%{?dist}
Summary:	Configures network time sync for use at Fermilab

%if 0%{?rhel} < 10
Obsoletes:	zz_ntp_configure
%endif

Group:		Fermilab
License:	GPL
URL:		https://github.com/fermilab-context-rpms/fermilab-conf_timesync
Source0:	chrony_fermilab_timesync.conf

BuildRequires:	bash coreutils systemd
BuildArch:	noarch

# Top level package should require software specific packages
Requires:	(%{name}-chrony == %{version}-%{release} if chrony)

%description
This package configures a time daemon correctly for use at Fermilab.

At this time the default time servers are listed as:
%{ntpservers}

%package chrony
Summary:	Configures chrony for use at Fermilab
Requires(post):	policycoreutils coreutils systemd grep
Requires:	chrony >= 3.0

%description chrony
This package configures chrony correctly for use at Fermilab.

At this time the default time servers are listed as:
%{ntpservers}


%prep


%build
touch fnal_timeservers.txt
for system in %{ntpservers}; do
  echo $system >> fnal_timeservers.txt
done

# chrony
mkdir chrony
cp %{SOURCE0} chrony/fermilab_timesettings.conf
echo "### THIS FILE IS MANAGED BY fermilab-conf_fermilab-conf_timesync-chrony ###" > chrony/fermilab_timeservers.conf
echo "###           YOUR CHANGES HERE WILL BE REVERTED BY THIS PACAKGE        ###" >> chrony/fermilab_timeservers.conf
for system in %{ntpservers}; do
    echo "server ${system} prefer iburst" >> chrony/fermilab_timeservers.conf
done


%install
%{__install} -D chrony/fermilab_timesettings.conf %{buildroot}/etc/chrony.d/fermilab_timesettings.conf
%{__install} -D chrony/fermilab_timeservers.conf %{buildroot}/etc/chrony.d/fermilab_timeservers.conf


%post chrony -p /usr/bin/bash
SELFCOPIES=${1:-0}

if [[ ${SELFCOPIES} -eq 1 ]]; then
    # start chrony
    systemctl enable chronyd.service
fi

grep -v '#' /etc/chrony.conf | grep -q 'include /etc/chrony.d/\*.conf'
if [[ $? -ne 0 ]]; then
  echo 'include /etc/chrony.d/*.conf' >> /etc/chrony.conf
fi

%postun chrony -p /usr/bin/bash
SELFCOPIES=${1:-0}


#####################################################################
#####################################################################
%files
%defattr(0644,root,root,0755)
%doc fnal_timeservers.txt

%files chrony
%defattr(0644,root,root,0755)
%config /etc/chrony.d/fermilab_timesettings.conf
%config /etc/chrony.d/fermilab_timeservers.conf

#####################################################################
%changelog
* Thu Apr 28 2022 Pat Riehecky <riehecky@fnal.gov> 1.0-7
- Set the FNAL servers to prefer

* Wed Apr 13 2022 Pat Riehecky <riehecky@fnal.gov> 1.0-6
- Drop SRV units since they no longer exist

* Wed Apr 13 2022 Pat Riehecky <riehecky@fnal.gov> 1.0-5.2
- Use boolean rich deps

* Wed Mar 16 2022 Pat Riehecky <riehecky@fnal.gov> 1.0-5
- Initial build for EL9

* Mon Jan 13 2020 Pat Riehecky <riehecky@fnal.gov> 1.0-4
- Initial build for EL8

* Mon Nov 2 2015 Pat Riehecky <riehecky@fnal.gov> 1.0-3
- now removes config on uninstall

* Thu Sep 24 2015 Pat Riehecky <riehecky@fnal.gov> 1.0-2.2
- better use of restorecon

* Tue Sep 8 2015 Pat Riehecky <riehecky@fnal.gov> 1.0-2.1
- Corrected second typo

* Tue Sep 8 2015 Pat Riehecky <riehecky@fnal.gov> 1.0-2
- Corrected typo

* Fri Aug 7 2015 Pat Riehecky <riehecky@fnal.gov> 1.0-1
- No broadcast client per RITM0096493
- Server list from RITM0096493
- Initial build for EL7
