%define _contrailetc  /etc/contrail
%define _distropkgdir %{_sbtop}tools/packages/rpm/%{name}
%define _opt_bin      /opt/contrail/bin
%define _usr_bin      /usr/bin/
%define _etc_init     /etc/init/
%define _supervisorconf /etc/contrail/supervisord_vrouter_files

%if 0%{?_buildTag:1}
%define _relstr %{_buildTag}
%else
%define _relstr %(date -u +%y%m%d%H%M)
%endif

%if 0%{?_srcVer:1}
%define _verstr %{_srcVer}
%else
%define _verstr 1
%endif

Name:    contrail-vrouter-dpdk-init
Version: %{_verstr}
Release: %{_relstr}%{?dist}
Summary: Contrail vrouter DPDK init %{?_gitVer}

Group:   Applications/System
License: Commercial
URL:     http://www.juniper.net/
Vendor:  Juniper Networks Inc

Requires: contrail-vrouter-dpdk >= %{_verstr}-%{_relstr}
Requires: contrail-vrouter-utils >= %{_verstr}-%{_relstr}
Requires: contrail-vrouter-agent
Requires: python-contrail-vrouter-api >= %{_verstr}-%{_relstr}
Requires: python-opencontrail-vrouter-netns >= %{_verstr}-%{_relstr}
Requires: supervisor

%description
Provides init files and utils for DPDK vRouter

%install
# Cleanup
rm -rf %{buildroot}

# Install Directories
install -d -m 755 %{buildroot}%{_opt_bin}
install -d -m 755 %{buildroot}%{_usr_bin}
install -d -m 755 %{buildroot}%{_contrailetc}
install -d -m 755 %{buildroot}%{_supervisorconf}
install -d -m 755 %{buildroot}/var/log/contrail/
install -d -m 755 %{buildroot}%{_etc_init}

# Install files
install -p -m 755 %{_distropkgdir}/dpdk_nic_bind.py %{buildroot}/%{_opt_bin}/dpdk_nic_bind.py
install -p -m 755 %{_distropkgdir}/ifquery %{buildroot}/%{_usr_bin}/ifquery
install -p -m 755 %{_distropkgdir}/contrail-vrouter-dpdk.ini %{buildroot}/%{_supervisorconf}/contrail-vrouter-dpdk.ini
install -p -m 755 %{_distropkgdir}/dpdk_vnagent_ExecStartPost.sh %{buildroot}/%{_contrailetc}/vnagent_ExecStartPost.sh
install -p -m 755 %{_distropkgdir}/dpdk_vnagent_ExecStartPre.sh %{buildroot}/%{_contrailetc}/vnagent_ExecStartPre.sh
install -p -m 755 %{_distropkgdir}/dpdk_vnagent_ExecStopPost.sh %{buildroot}/%{_contrailetc}/vnagent_ExecStopPost.sh
install -p -m 755 %{_distropkgdir}/contrail_reboot %{buildroot}/%{_contrailetc}/contrail_reboot
install -p -m 755 %{_distropkgdir}/vrouter-functions.sh %{buildroot}%{_opt_bin}/vrouter-functions.sh
install -p -m 755 %{_distropkgdir}/vnagent_param_setup.sh %{buildroot}%{_opt_bin}/vnagent_param_setup.sh
install -p -m 755 %{_distropkgdir}/contrail-vrouter-dpdk.rules %{buildroot}/%{_supervisorconf}/contrail-vrouter-dpdk.rules
install -p -m 755 %{_distropkgdir}/if-vhost0 %{buildroot}%{_opt_bin}/if-vhost0
install -p -m 755 %{_distropkgdir}/core-pattern.upstart %{buildroot}%{_etc_init}/core-pattern.conf

%files
%defattr(-,root,root,-)
%{_opt_bin}/*
%{_usr_bin}/*
%{_contrailetc}/*
%{_supervisorconf}/*
%{_etc_init}/*

%post
echo "Running Postinst for contrail-vrouter-dpkd-init"
echo "create /etc/contrail/agent_param.tmpl"
/opt/contrail/bin/vnagent_param_setup.sh
echo "Postinst for contrail-vrouter-dpdk-init done"

%preun
# Remove /etc/contrail/agent_param.tmpl created during postinstall script
if [ -f /etc/contrail/agent_param.tmpl ]; then
    rm -f /etc/contrail/agent_param.tmpl
fi

%changelog
* Thu Feb 16 2017 Nagendra Maynattamai <npchandran@juniper.net> 4.1.1-2.1contrail1
- Initial Build for Opencontrail
