from . import TestController

from sword2 import Entry
from sword2.utils import NS

class TestEntry(TestController):
    def test_01_blank_init(self):
        e = Entry()
        print(e.entry.getchildren())
        assert len(e.entry.getchildren()) == 2   # generator, updated are there by default
    
    def test_02_init_without_author(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", dcterms_title="foo bar")
        assert e.entry.find(NS['atom'].format('title')) != None
        assert e.entry.find(NS['dcterms'].format('appendix')) != None
        assert e.entry.find(NS['dcterms'].format('nonexistant_term')) == None
        
    def test_03_init_with_author(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", author={'name':'Ben', 'email':'foo@bar.com'})
        assert e.entry.find(NS['atom'].format('title')) != None
        assert e.entry.find(NS['atom'].format('title')).text == "Foo"
        a = e.entry.find(NS['atom'].format('author'))
        name = a.find(NS['atom'].format('name'))
        assert name.text == "Ben"
    
    def test_04_init_add_namespace(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", author={'name':'Ben', 'email':'foo@bar.com'})
        e.register_namespace("mylocal", "info:localnamespace")
        assert "mylocal" in e.add_ns
        
    def test_05_init_add_fields(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", author={'name':'Ben', 'email':'foo@bar.com'})
        e.add_field("dcterms_issued", "2009")
        assert e.entry.find(NS['dcterms'].format('issued')) != None
        assert e.entry.find(NS['dcterms'].format('issued')).text == "2009"
        
    def test_06_init_add_fields(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", author={'name':'Ben', 'email':'foo@bar.com'})
        e.add_fields(dcterms_issued="2009",
                     updated="2010",
                     dcterms_description="A verbose and new description")
        
        assert e.entry.find(NS['atom'].format('updated')) != None
        assert e.entry.find(NS['atom'].format('updated')).text == "2010"
        assert e.entry.find(NS['dcterms'].format('issued')) != None
        assert e.entry.find(NS['dcterms'].format('issued')).text == "2009"
        assert e.entry.find(NS['dcterms'].format('description')) != None
        assert e.entry.find(NS['dcterms'].format('description')).text == "A verbose and new description"
        
        
    def test_07_init_add_new_ns_field(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", author={'name':'Ben', 'email':'foo@bar.com'})
        e.register_namespace("mylocal", "info:localnamespace")
        e.add_field("mylocal_issued", "2003")
        assert e.entry.find(NS['mylocal'].format('issued')) != None
        assert e.entry.find(NS['mylocal'].format('issued')).text == "2003"
        
    def test_08_init_add_new_ns_fields(self):
        e = Entry(title="Foo", id="asidjasidj", dcterms_appendix="blah blah", author={'name':'Ben', 'email':'foo@bar.com'})
        e.register_namespace("mylocal", "info:localnamespace")
        e.add_fields(mylocal_foobar="2009",
                     updated="2010",
                     mylocal_description="A verbose and new description")
        
        assert e.entry.find(NS['atom'].format('updated')) != None
        assert e.entry.find(NS['atom'].format('updated')).text == "2010"
        assert e.entry.find(NS['mylocal'].format('foobar')) != None
        assert e.entry.find(NS['mylocal'].format('foobar')).text == "2009"
        assert e.entry.find(NS['mylocal'].format('description')) != None
        assert e.entry.find(NS['mylocal'].format('description')).text == "A verbose and new description"
