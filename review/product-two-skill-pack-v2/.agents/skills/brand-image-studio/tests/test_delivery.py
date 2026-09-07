"""Synthetic file fixtures test delivery gates, not native generation or visual quality."""
from pathlib import Path
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify_delivery', SKILL/'scripts/verify_delivery.py')
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)

class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        Image.new('RGB', (1080,1350), '#234567').save(self.root/'output.png')
        for name in ['tool-contract.md','tool-result.md','text-review.md','visual-review.md','size-source.md']:
            (self.root/name).write_text('Synthetic regression evidence only: populated test fixture, not a real tool or visual review.')
        digest = gate.sha256(self.root/'output.png')
        self.request = {'schema_version':1,'platform':'Instagram','placement':'lesson3-carousel','width':1080,'height':1350,'aspect_ratio':[4,5],'basis':'project_brief','evidence':'size-source.md'}
        self.record = {'schema_version':2,'skill':{'name':'brand-image-studio','sha256':gate.sha256(gate.SKILL_FILE)},'operation':'create','request_file':'request.json','target':{'width':1080,'height':1350},'tool':{'name':'fixture-tool','mode':'native-generate','parameters':{},'size_control':'structured','evidence':'tool-contract.md'},'generation_evidence':'tool-result.md','output_image':'output.png','output_sha256':digest,'reviews':{kind:{'status':'pass','image_sha256':digest,'evidence':kind+'-review.md'} for kind in ['text','visual']}}
        self.save_request()
    def save_request(self):
        (self.root/'request.json').write_text(json.dumps(self.request))
        self.record['request_sha256']=gate.sha256(self.root/'request.json')
    def tearDown(self):
        self.tmp.cleanup()
    def verify(self):
        (self.root/'delivery.json').write_text(json.dumps(self.record))
        return gate.verify(self.root/'delivery.json')
    def test_exact_file_passes_local_gate_without_approval_claim(self):
        r=self.verify();self.assertTrue(r['ok'],r);self.assertEqual(r['status'],'LOCAL_QA_PASSED_REVIEW_REQUIRED')
    def test_missing_target_fails(self):
        self.record.pop('target');self.assertFalse(self.verify()['ok'])
    def test_target_cannot_be_changed_to_fit_wrong_output(self):
        Image.new('RGB',(1023,1537),'white').save(self.root/'output.png');self.record['target']={'width':1023,'height':1537};d=gate.sha256(self.root/'output.png');self.record['output_sha256']=d
        for review in self.record['reviews'].values():review['image_sha256']=d
        self.assertTrue(any('differs from the pre-generation request' in e for e in self.verify()['errors']))
    def test_landscape_does_not_pass_portrait_target(self):
        Image.new('RGB',(1350,1080),'white').save(self.root/'output.png');self.assertTrue(any('size mismatch' in e for e in self.verify()['errors']))
    def test_edit_invalidates_previous_review_even_at_same_size(self):
        Image.new('RGB',(1080,1350),'#555555').save(self.root/'output.png');self.record['output_sha256']=gate.sha256(self.root/'output.png');r=self.verify();self.assertFalse(r['ok']);self.assertTrue(any('review does not match' in e for e in r['errors']))
    def test_stale_skill_version_rejected(self):
        self.record['skill']['sha256']='0'*64;self.assertFalse(self.verify()['ok'])
    def test_logo_edit_requires_input_and_new_reviews(self):
        self.record['operation']='add-logo';self.record['tool']['mode']='native-edit';self.assertFalse(self.verify()['ok'])
        Image.new('RGB',(1080,1350),'#000000').save(self.root/'input.png');self.record['input_image']='input.png';self.record['input_sha256']=gate.sha256(self.root/'input.png');self.assertTrue(self.verify()['ok'])
    def test_stretch_cannot_pass_as_proportional_resize(self):
        Image.new('RGB',(1023,1537),'white').save(self.root/'input.png');self.record['tool']['mode']='proportional-resize';self.record.update(operation='resize',input_image='input.png',input_sha256=gate.sha256(self.root/'input.png'));self.assertTrue(any('resize changed aspect' in e for e in self.verify()['errors']))
    def test_pending_or_empty_review_rejected(self):
        self.record['reviews']['text']['status']='pending';self.assertFalse(self.verify()['ok']);self.record['reviews']['text']['status']='pass';(self.root/'text-review.md').write_text('PASS');self.assertFalse(self.verify()['ok'])
    def test_corrupt_image_fails(self):
        (self.root/'output.png').write_bytes(b'fake PNG');self.assertFalse(self.verify()['ok'])
    def test_outside_job_path_rejected(self):
        self.record['output_image']='../output.png';self.assertFalse(self.verify()['ok'])
    def test_symlink_rejected(self):
        (self.root/'alias.png').symlink_to(self.root/'output.png');self.record['output_image']='alias.png';self.assertFalse(self.verify()['ok'])
    def test_banner_uses_explicit_dimensions(self):
        Image.new('RGB',(1200,630),'white').save(self.root/'output.png');d=gate.sha256(self.root/'output.png');self.record.update(format='seo-banner',target={'width':1200,'height':630},output_sha256=d)
        for review in self.record['reviews'].values():review['image_sha256']=d
        self.request.update(platform='Website',placement='hero',width=1200,height=630,basis='user_explicit');self.request.pop('aspect_ratio');self.save_request()
        self.assertTrue(self.verify()['ok'])
    def test_inspector_requires_explicit_check_mode(self):
        args=[sys.executable,str(SKILL/'scripts/inspect_images.py'),str(self.root/'output.png')]
        self.assertNotEqual(subprocess.run(args,capture_output=True).returncode,0)
        r=subprocess.run(args+['--metadata-only'],capture_output=True,text=True);self.assertEqual(r.returncode,0);data=json.loads(r.stdout);self.assertFalse(data['target_checked']);self.assertFalse(data['delivery_ready'])
    def test_cli_preserves_existing_check_receipt(self):
        self.verify();out=self.root/'check.json';out.write_text('keep');r=subprocess.run([sys.executable,str(SKILL/'scripts/verify_delivery.py'),str(self.root/'delivery.json'),'--output',str(out)],capture_output=True);self.assertNotEqual(r.returncode,0);self.assertEqual(out.read_text(),'keep')

    def test_square_ig_and_vertical_story_accept_explicit_user_sizes(self):
        for width,height,placement in [(1080,1080,'feed-square'),(1080,1920,'story')]:
            with self.subTest(placement=placement):
                self.request.update(width=width,height=height,placement=placement,basis='user_explicit')
                self.request.pop('aspect_ratio',None);self.save_request()
                Image.new('RGB',(width,height),'white').save(self.root/'output.png')
                digest=gate.sha256(self.root/'output.png')
                self.record.update(target={'width':width,'height':height},output_sha256=digest)
                for review in self.record['reviews'].values():review['image_sha256']=digest
                result=self.verify();self.assertTrue(result['ok'],result)
    def test_arbitrary_custom_dimensions_are_not_a_platform_enum(self):
        self.request.update(platform='custom',placement='user-specified image',basis='user_explicit')
        self.save_request();self.assertTrue(self.verify()['ok'])
    def test_ambiguous_request_asks_without_reading_an_output_image(self):
        (self.root/'output.png').unlink();self.request.pop('width');self.request.pop('height');self.request['placement']='TBC';self.save_request()
        result=gate.verify_request(self.root/'request.json');self.assertEqual(result['status'],'ASK_USER')
        self.assertTrue(any('pixel width' in e for e in result['errors']))
    def test_ratio_only_and_unconfirmed_suggestion_do_not_pass_preflight(self):
        self.request.pop('width');self.request.pop('height');self.request['basis']='pending';self.save_request()
        result=gate.verify_request(self.root/'request.json');self.assertFalse(result['ok']);self.assertTrue(any('confirm' in e for e in result['errors']))
    def test_conflicting_ratio_and_pixels_asks_before_generation(self):
        self.request['aspect_ratio']=[9,16];self.save_request()
        result=gate.verify_request(self.root/'request.json');self.assertEqual(result['status'],'ASK_USER');self.assertTrue(any('conflicts' in e for e in result['errors']))
    def test_request_change_invalidates_delivery(self):
        self.request['placement']='new use';(self.root/'request.json').write_text(json.dumps(self.request))
        self.assertTrue(any('request hash' in e for e in self.verify()['errors']))
    def test_wrong_mode_for_edit_is_blocked(self):
        self.record['operation']='add-logo'
        self.assertTrue(any('tool mode' in e for e in self.verify()['errors']))
    def test_recompose_requires_original_and_its_own_mode(self):
        self.record['operation']='recompose';self.record['tool']['mode']='native-recompose'
        self.assertFalse(self.verify()['ok'])
        Image.new('RGB',(1080,1920),'white').save(self.root/'input.png')
        self.record.update(input_image='input.png',input_sha256=gate.sha256(self.root/'input.png'))
        self.assertTrue(self.verify()['ok'])
    def test_preflight_cli_reports_request_ready_without_generation(self):
        (self.root/'output.png').unlink()
        result=subprocess.run([sys.executable,str(SKILL/'scripts/verify_delivery.py'),str(self.root/'request.json'),'--preflight'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout)['status'],'REQUEST_READY')
    def test_missing_actual_parameters_blocks_delivery(self):
        self.record['tool'].pop('parameters');self.assertFalse(self.verify()['ok'])
    def test_boolean_or_zero_pixel_values_rejected(self):
        for width in [True,0,-1,'1080']:
            self.request['width']=width;self.save_request();self.assertFalse(gate.verify_request(self.root/'request.json')['ok'])

if __name__ == '__main__':
    unittest.main()
