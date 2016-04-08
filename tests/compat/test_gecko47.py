from helper import CompatTestCase
from validator.compat import FX47_DEFINITION


class TestFX47Compat(CompatTestCase):
    """Test that compatibility tests for Gecko 47 are properly executed."""

    VERSION = FX47_DEFINITION

    def test_bnsIX509CertDB_method_changed(self):
        """https://github.com/mozilla/addons-server/issues/2221"""
        expected = 'Most methods in nsIX509CertDB had their unused arguments removed.'

        script = '''
            var certDB = Cc["@mozilla.org/security/x509certdb;1"]
                    .getService(Ci.nsIX509CertDB);
            certDB.importPKCS12File(null, nsIFile);
        '''

        self.run_script_for_compat(script)

        assert not self.compat_err.notices
        assert not self.compat_err.errors

        # There are other checks because using nsIX509CertDB is
        # potentially dangerous.
        assert len(self.compat_err.warnings) == 4
        assert self.compat_err.warnings[3]['compatibility_type'] == 'error'
        assert self.compat_err.warnings[3]['message'].startswith(expected)

        script = '''
            var certDB = Cc["@mozilla.org/security/x509certdb;1"]
                                        .getService(Ci.nsIX509CertDB);
            certdb.importCertsFromFile(null, fp.file, nsIX509Cert.CA_CERT);
        '''

        self.reset()
        self.run_script_for_compat(script)

        assert not self.compat_err.notices
        assert not self.compat_err.errors

        # There are other checks because using nsIX509CertDB is
        # potentially dangerous.
        assert len(self.compat_err.warnings) == 4
        assert self.compat_err.warnings[3]['compatibility_type'] == 'error'
        assert self.compat_err.warnings[3]['message'].startswith(expected)

        script = 'const nsIX509CertDB = Components.interfaces.nsIX509CertDB;'

        self.reset()
        self.run_script_for_compat(script)

        assert not self.compat_err.notices
        assert not self.compat_err.errors

        # There are other checks because using nsIX509CertDB is
        # potentially dangerous.
        assert len(self.compat_err.warnings) == 3
        assert self.compat_err.warnings[2]['compatibility_type'] == 'error'
        assert self.compat_err.warnings[2]['message'].startswith(expected)
