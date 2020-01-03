# Copyright (c) 2011-2012 OpenStack Foundation
# All Rights Reserved.
# 
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
##################################
#
#    Copyright (c) crazy@geeks.pl 
#
#    Isolate given teenants to configured aggregates only.
#
#    Needs metadata on host aggregate:  'filter_tenant_id=xxx,yyy'
#
#    To do: 
#    - move isolated_tenants to config 
#
#    Tested on Ocata-Queens
##################################     

from nova.scheduler import filters
from oslo_log import log as logging
from nova.scheduler.filters import utils

LOG = logging.getLogger(__name__)

isolated_tenants =  ["7c4481d152f949afaddd1f02de1e53ea"]

class IsolatedTenantFilter(filters.BaseHostFilter):
    """Keep specified images to selected hosts."""

    # The configuration values do not change within a request
    run_filter_once_per_request = True

    RUN_ON_REBUILD = True
    def host_passes(self, host_state, spec_obj):
        # If the configuration does not list any hosts, the filter will always
        # return True, assuming a configuration error, so letting all hosts
        # through.

        tenant_id = spec_obj.project_id

        if not isolated_tenants:
            # As there are no images to match, return True if the filter is
            # not restrictive otherwise return False if the host is in the
            # isolation list.
            LOG.debug("There is no configured isolation globally");
            return True 

        if tenant_id not in isolated_tenants:
            LOG.debug("Tenant doesn't need an isolation");
            return True

        metadata = utils.aggregate_metadata_get_by_host(host_state,
                                                       key="filter_tenant_id")
        if metadata != {}:
            configured_tenant_ids = metadata.get("filter_tenant_id")
            LOG.debug("configured filter %s on host %s", configured_tenant_ids, host_state)
            if configured_tenant_ids:
                if tenant_id not in configured_tenant_ids:
                    LOG.debug("NOT matched tenant_id on aggregate %s", host_state)
                    return False
                LOG.debug("Matched for tenant %s", tenant_id)
                return True
            else:
                LOG.debug("No tenant id's defined on host. Skipping")
                return False
        return False
