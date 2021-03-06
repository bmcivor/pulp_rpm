import shutil
import tempfile
import unittest

import mock

from pulp_rpm.plugins.distributors.yum.metadata.primary import PrimaryXMLFileContext


class PrimaryXMLFileContextTests(unittest.TestCase):
    def setUp(self):
        self.working_dir = tempfile.mkdtemp()
        self.context = PrimaryXMLFileContext(self.working_dir, 3, checksum_type='sha256')
        self.unit = mock.Mock()
        self.unit.render_primary.return_value = 'somexml'

    def tearDown(self):
        shutil.rmtree(self.working_dir)

    def test_init(self):
        self.assertEquals(self.context.fast_forward, False)
        self.assertEquals(self.context.num_packages, 3)

    def test_add_unit_metadata(self):
        self.context.metadata_file_handle = mock.Mock()
        self.context.add_unit_metadata(self.unit)
        self.context.metadata_file_handle.write.assert_called_once_with('somexml')
        self.unit.render_primary.assert_called_once_with('sha256')

    def test_add_unit_metadata_unicode(self):
        """
        Test that the primary repodata is passed as a str even if it's a unicode object.
        """
        self.context.metadata_file_handle = mock.Mock()
        expected_call = u'some unicode'
        self.unit.render_primary.return_value = expected_call
        self.context.add_unit_metadata(self.unit)
        self.context.metadata_file_handle.write.assert_called_once_with(expected_call)
        self.unit.render_primary.assert_called_once_with('sha256')
