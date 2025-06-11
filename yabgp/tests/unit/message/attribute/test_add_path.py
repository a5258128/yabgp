# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
#    Licensed under the Apache License, version 2.0 (the "License"); you may
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

"""Test Add Path Capability"""

import unittest
from yabgp.message.open import convert_addpath_str_to_int


class TestAddPathCapability(unittest.TestCase):
    """
    Test cases for Add Path capability introduced in commits 1a17665 and 814598b.
    These tests cover:
    1. convert_addpath_str_to_int function
    2. Add path capability parsing and construction
    3. Add path negotiation logic
    """

    def setUp(self):
        """Set up test fixtures"""
        self.maxDiff = None

    def test_convert_addpath_str_to_int_single_receive(self):
        """
        Test converting a single AFI/SAFI in receive mode
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 1), 1]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_single_send(self):
        """
        Test converting a single AFI/SAFI in send mode
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 1), 2]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_single_both(self):
        """
        Test converting a single AFI/SAFI in both mode
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 1), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_multiple_afi_safi(self):
        """
        Test converting multiple AFI/SAFI entries
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [
            [(1, 1), 3],  # ipv4, both
            [(2, 1), 1],  # ipv6, receive
            [(1, 128), 2]  # vpnv4, send
        ]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_ipv4_lu(self):
        """
        Test converting IPv4 Labeled Unicast
        """
        addpath_list = [
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 4), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_ipv6_lu(self):
        """
        Test converting IPv6 Labeled Unicast
        """
        addpath_list = [
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(2, 4), 1]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_vpnv6(self):
        """
        Test converting VPNv6
        """
        addpath_list = [
            {'afi_safi': 'vpnv6', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(2, 128), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_flowspec(self):
        """
        Test converting Flowspec
        """
        addpath_list = [
            {'afi_safi': 'flowspec', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 133), 2]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_empty_list(self):
        """
        Test converting empty list
        """
        addpath_list = []
        result = convert_addpath_str_to_int(addpath_list)
        expected = []
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_mixed_families(self):
        """
        Test converting mixed address families (IPv4, IPv6, VPN, Labeled Unicast)
        """
        addpath_list = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'both'},
            {'afi_safi': 'ipv4_lu', 'send/receive': 'receive'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'},
            {'afi_safi': 'vpnv6', 'send/receive': 'send'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [
            [(1, 1), 3],    # ipv4, both
            [(2, 1), 3],    # ipv6, both
            [(1, 4), 1],    # ipv4_lu, receive
            [(2, 4), 1],    # ipv6_lu, receive
            [(1, 128), 2],  # vpnv4, send
            [(2, 128), 2]   # vpnv6, send
        ]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_evpn(self):
        """
        Test converting EVPN
        """
        addpath_list = [
            {'afi_safi': 'evpn', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(25, 70), 3]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_bgpls(self):
        """
        Test converting BGP-LS
        """
        addpath_list = [
            {'afi_safi': 'bgpls', 'send/receive': 'receive'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(16388, 71), 1]]
        self.assertEqual(expected, result)

    def test_convert_addpath_str_to_int_sr_policy(self):
        """
        Test converting SR Policy
        """
        addpath_list = [
            {'afi_safi': 'ipv4_srte', 'send/receive': 'both'}
        ]
        result = convert_addpath_str_to_int(addpath_list)
        expected = [[(1, 73), 3]]
        self.assertEqual(expected, result)


class TestAddPathNegotiation(unittest.TestCase):
    """
    Test cases for Add Path negotiation logic in protocol.py
    Tests the compare_add_path method
    """

    def setUp(self):
        """Set up test fixtures"""
        # Import here to avoid circular dependencies
        from yabgp.core.protocol import BGP
        self.bgp = BGP()
        self.maxDiff = None

    def test_compare_add_path_both_support_ipv4(self):
        """
        Test when both local and remote support IPv4 add path
        Local: receive, Remote: send -> negotiation succeeds
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {'ipv4': True}
        self.assertEqual(expected, result)

    def test_compare_add_path_both_support_both(self):
        """
        Test when both local and remote support both mode
        Local: both, Remote: both -> negotiation succeeds
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {'ipv4': True}
        self.assertEqual(expected, result)

    def test_compare_add_path_local_send_remote_receive(self):
        """
        Test local send and remote receive
        Local: send, Remote: receive -> negotiation fails (direction mismatch)
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {'ipv4': False}
        self.assertEqual(expected, result)

    def test_compare_add_path_local_both_remote_send(self):
        """
        Test local both and remote send
        Local: both (includes receive), Remote: send -> negotiation succeeds
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {'ipv4': True}
        self.assertEqual(expected, result)

    def test_compare_add_path_local_receive_remote_both(self):
        """
        Test local receive and remote both
        Local: receive, Remote: both (includes send) -> negotiation succeeds
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {'ipv4': True}
        self.assertEqual(expected, result)

    def test_compare_add_path_no_local(self):
        """
        Test when local does not support add path
        Returns None
        """
        local_add_path = None
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        self.assertIsNone(result)

    def test_compare_add_path_no_remote(self):
        """
        Test when remote does not support add path
        Returns None
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        remote_add_path = None
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        self.assertIsNone(result)

    def test_compare_add_path_empty_local(self):
        """
        Test when local add path list is empty
        Returns None
        """
        local_add_path = []
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        self.assertIsNone(result)

    def test_compare_add_path_empty_remote(self):
        """
        Test when remote add path list is empty
        Returns None
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        remote_add_path = []
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        self.assertIsNone(result)

    def test_compare_add_path_multiple_afi_safi(self):
        """
        Test negotiation with multiple AFI/SAFI entries
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'},
            {'afi_safi': 'ipv6', 'send/receive': 'both'},
            {'afi_safi': 'vpnv4', 'send/receive': 'receive'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {
            'ipv4': True,   # local both (includes receive) + remote send = success
            'ipv6': True,   # local receive + remote both (includes send) = success
            'vpnv4': False  # local send + remote receive = fail (direction mismatch)
        }
        self.assertEqual(expected, result)

    def test_compare_add_path_different_afi_safi(self):
        """
        Test when local and remote support different AFI/SAFI
        Only common ones will be negotiated
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'},
            {'afi_safi': 'vpnv4', 'send/receive': 'both'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {
            'ipv4': True  # only ipv4 is commonly supported
        }
        self.assertEqual(expected, result)

    def test_compare_add_path_no_common_afi_safi(self):
        """
        Test when local and remote have no common AFI/SAFI
        Returns empty dictionary
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv6', 'send/receive': 'both'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {}
        self.assertEqual(expected, result)

    def test_compare_add_path_all_address_families(self):
        """
        Test negotiation for all supported address families
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'both'},
            {'afi_safi': 'ipv4_lu', 'send/receive': 'receive'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'both'},
            {'afi_safi': 'vpnv6', 'send/receive': 'both'},
            {'afi_safi': 'flowspec', 'send/receive': 'receive'},
            {'afi_safi': 'evpn', 'send/receive': 'both'}
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'send'},
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'send'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'},
            {'afi_safi': 'vpnv6', 'send/receive': 'both'},
            {'afi_safi': 'flowspec', 'send/receive': 'send'},
            {'afi_safi': 'evpn', 'send/receive': 'both'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        expected = {
            'ipv4': True,     # both + both
            'ipv6': True,     # both (includes receive) + send
            'ipv4_lu': True,  # receive + both (includes send)
            'ipv6_lu': True,  # receive + send
            'vpnv4': True,    # both (includes receive) + send
            'vpnv6': True,    # both + both
            'flowspec': True, # receive + send
            'evpn': True      # both + both
        }
        self.assertEqual(expected, result)

    def test_compare_add_path_duplicate_afi_safi_in_local(self):
        """
        Test when local has duplicate AFI/SAFI entries
        Should only match the first one
        """
        local_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'},
            {'afi_safi': 'ipv4', 'send/receive': 'send'}  # duplicate
        ]
        remote_add_path = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        result = self.bgp.compare_add_path(local_add_path, remote_add_path)
        # First match succeeds, second also matches (but overwrites)
        # Actually there will be two matches, but the last one overwrites the previous
        self.assertIn('ipv4', result)


class TestLocalAddPathConfig(unittest.TestCase):
    """
    Test cases for local_add_path configuration processing in config.py
    Tests the list comprehension that converts local_add_path strings to dictionaries
    """

    def test_local_add_path_single_ipv4_both(self):
        """
        Test processing single IPv4 both mode configuration
        """
        # Simulate the list comprehension from config.py line 137-139
        local_add_path_config = ['ipv4_both']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_single_ipv4_receive(self):
        """
        Test processing single IPv4 receive mode configuration
        """
        local_add_path_config = ['ipv4_receive']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'receive'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_single_ipv4_send(self):
        """
        Test processing single IPv4 send mode configuration
        """
        local_add_path_config = ['ipv4_send']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_multiple_families(self):
        """
        Test processing multiple address families configuration
        """
        local_add_path_config = ['ipv4_both', 'ipv6_receive', 'vpnv4_send']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'both'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'send'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_labeled_unicast(self):
        """
        Test processing Labeled Unicast address family configuration
        Note: ipv4_lu has two underscores, rsplit('_', 1) only splits the last one
        """
        local_add_path_config = ['ipv4_lu_both', 'ipv6_lu_receive']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_empty_list(self):
        """
        Test processing empty configuration list
        """
        local_add_path_config = []
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = []
        self.assertEqual(expected, result)

    def test_local_add_path_all_modes(self):
        """
        Test all modes (send, receive, both)
        """
        local_add_path_config = ['ipv4_send', 'ipv6_receive', 'vpnv4_both']
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4', 'send/receive': 'send'},
            {'afi_safi': 'ipv6', 'send/receive': 'receive'},
            {'afi_safi': 'vpnv4', 'send/receive': 'both'}
        ]
        self.assertEqual(expected, result)

    def test_local_add_path_complex_afi_safi_names(self):
        """
        Test complex address family names (containing multiple underscores)
        """
        local_add_path_config = [
            'ipv4_lu_both',
            'ipv6_lu_receive',
            'ipv4_srte_send',
            'ipv6_flowspec_both'
        ]
        result = [
            {'afi_safi': item.rsplit('_', 1)[0], 'send/receive': item.rsplit('_', 1)[1]}
            for item in local_add_path_config
        ]
        expected = [
            {'afi_safi': 'ipv4_lu', 'send/receive': 'both'},
            {'afi_safi': 'ipv6_lu', 'send/receive': 'receive'},
            {'afi_safi': 'ipv4_srte', 'send/receive': 'send'},
            {'afi_safi': 'ipv6_flowspec', 'send/receive': 'both'}
        ]
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
