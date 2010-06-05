"""
Form Utils.

Contains useful classes and functions to help with the maintenance of data collections and sets.
"""
from django import forms

class SetItemForm(forms.Form):
  """Base class for all forms that are set items"""
  id = forms.IntegerField(widget=forms.HiddenInput, required=False)
  order = forms.IntegerField(widget=forms.HiddenInput, required=False)
  delete = forms.BooleanField(widget=forms.HiddenInput, required=False)

  def __cmp__(self, other):
    """Compare two items by order.  Expects cleaned_data to be set.  Blank goes after number."""
    return cmp(self.cleaned_data.get('order') or '', other.cleaned_data.get('order') or '')

class CollectionForm(forms.BaseForm):
  """
  A special kind of Form (based off BaseForm) that creates fields during class instantiation rather 
  than during class declaration.  Uses additional (required) parameters during instantiation.
  """

  class PrefixRequiredException(Exception): pass

  def __init__(self, data=None, *args, **kwargs):
    """
    Accepts additional named parameters:
    - collection_count : max # of items in collection
    - collection_choices : sequence of (k,v) tuples
    - collection_values : initial values
    Requires 'prefix' to be passed.
    """

    if 'prefix' not in kwargs: raise PrefixRequiredException()
    self.prefix = kwargs['prefix']  # need to do this early cause we want to use 'add_prefix' method

    self.base_fields = {}
    self.collection_count = 0

    self.collection_required = bool(kwargs.get('collection_required'))

    values = {}
    if 'collection_values' in kwargs:
      vl = kwargs['collection_values']
      if not isinstance(vl, (tuple,list)):
        raise exceptions.TypeError('collection_values parameter must be a sequence')
      for idx,v in enumerate(vl):
        values[self.add_prefix("coll%d" % (idx+1,))] = v

    if 'collection_count' in kwargs:
      self.collection_count = kwargs['collection_count']
      if not isinstance(self.collection_count, int): 
        raise exceptions.TypeError('collection_count parameter must be integer')
      choices = kwargs.get('collection_choices', [])
      if not isinstance(choices, (list, tuple)):
        raise exceptions.TypeError('collection_choices parameter must be sequence of 2-tuples')
      choices_d = kwargs.get('collection_choices_byidx', {})
      if not isinstance(choices_d, dict):
        raise exceptions.TypeError('collection_choices_byidx parameter must be dict')
      choices_d[0] = choices
      initialvalues = (data or values or {})
      for i in range(self.collection_count):
        name = 'coll%d' % (i+1,)
        initial = initialvalues.get(self.add_prefix(name), None)
        field = forms.ChoiceField(required=False, choices=choices_d.get(i+1, choices_d[0]), initial=initial)
        self.base_fields[name] = field

    for kw in ('collection_count', 'collection_choices', 'collection_values', 'collection_choices_byidx', 'collection_required'):
      if kw in kwargs: del kwargs[kw]

    super(CollectionForm, self).__init__(data, *args, **kwargs)

  def enumerate(self):
    for idx,name in enumerate(sorted(self.fields.keys())):
      yield (idx+1, self[name])

  def clean(self):
    cleaned_data = self.cleaned_data
    print "CollectionForm(prefix=%s).clean(): required=%s" % (self.prefix, self.collection_required)
    if self.collection_required:
      data = filter(None, [ cleaned_data.get('coll%d' % (idx+1,)) for idx in range(self.collection_count) ])
      if not data: raise forms.ValidationError('This field is required')
    return cleaned_data

# UPDATE SET:
def updateSet(instance, rel, fkname, formset, data_changed, data_update, data_blank, rel_filter=None):
  """
  Logic to update generic data sets.
  Requires:
  - instance : instance that holds set to update
  - rel : relation to update
  - fkname : name of foreign key field in relation (set) model
  - formset : form set instance (data) that will be used to update database
  - data_changed : function to use when detecting if data has changed
  - data_update : function to use to update data (set fields for update or insert)
  - data_blank : function to use to determine if data is blank
  - rel_filter : filter to apply to relation to find eligible rows to update
  Will use formset data to update data set for a given model with respect to a given instance.  Does a 
  proper "sync", ie. it doesn't just delete and re-create everything.  
  """

  model = rel.model
  which = rel.model.__name__
  ordered = hasattr(model, 'order')

  if rel_filter:
    curvalues = rel.filter(**rel_filter)
  else:
    curvalues = rel.all()
  curvalues_d = dict( [ (_.id, _) for _ in curvalues ] )
  curids = curvalues_d.keys()  # Keep track of what we need to remove afterwards

  print "PROCESSING SET: ", which
  print "> current ids:", curids

  # Sort forms by order (helps validating order #s after)
  allforms = list(formset.forms)
  allforms.sort()

  # Process all forms
  order = 1
  for form in allforms:
    data = form.cleaned_data
    # If empty form, skip it
    if not data:
      continue
    print "> FOUND: id=%s, order=%s, delete=%s" % (data['id'], data['order'], data['delete'])
    # If we have an id and its not part of current instance, raise tampering error
    if data['id'] and data['id'] not in curids:
      raise Exception('Detected form tampering during instance save: instance id# %d has no %s id# %d' % (instance.id, which, data['id']))
    if data['id']:
      # Operation: update/delete
      row = curvalues_d[data['id']]
      if data['delete'] or data_blank(data):
        print "- Removing %s id# %s" % (which, row.id)
        row.delete()
      else:
        if (ordered and row.order != order) or getattr(row,'stage', 1) != 1 or data_changed(row, data):
          print "- Update %s id# %s" % (which, row.id)
          if ordered: row.order = order
          data_update(row, data)
          row.save()
        else:
          print "- Skipping unchanged %s id# %s" % (which, row.id)
          pass
        order += 1
      curids.remove(data['id'])
    elif not data_blank(data) and not data['delete']:
      # Operation: add
      print "- Adding %s id# %s" % (which, "???")
      row = model(**{ fkname: instance })
      if ordered: row.order = order
      data_update(row, data)
      row.save()
      print "- Added as id=%s" % (row.id,)
      order += 1

  # Remove items that disappeared from form (shouldn't happen, but...)
  for curid in curids:
    row = curvalues_d[curid]
    print "- REMOVING unknown %s id# %s" % (which, row.id)
    row.delete()

  # Done: updateSet.

def makesetdata(row):
  return dict(id=row.id, order=getattr(row, 'order', 0), delete='')

def updateRelations(rel, table, maxvalues, form, rel_filter=None):
  """
  Logic to update generic relations.
  Requires:
  - rel : relation to update
  - table: database model
  - maxvalues : maximum # of relations to support
  - form : CollecitonForm instance
  - rel_filter : filter to apply to relation to find eligible rows to update
  Will use CollectionForm data to update relations for a given model.  Does a proper "sync", ie. 
  it doesn't just delete and re-create everything (although it wouldn't be a big deal, as its
  just relations that are updated, not actual objects).
  """

  if rel_filter and isinstance(rel_filter, dict): curvalues = rel.filter(**rel_filter)
  else: curvalues = rel.all()
  curvalues_d = dict( [ (_.id, _) for _ in curvalues ] )
  curids = curvalues_d.keys()  # Keep track of what we need to remove afterwards
  newvalues = filter(None, map(siteutils.to_int, form.cleaned_data.values()))
  for idx0 in range(min(len(newvalues), maxvalues)):
    vid = newvalues[idx0]
    if not vid: continue
    idx = idx0+1
    if vid in curvalues_d:
      if vid in curids: curids.remove(vid)  # Just in case we try to remove twice!
      continue
    q = table.objects.filter(id=vid) or None
    if not q:
      continue
    rel.add(q[0])
  for vid in curids:
    rel.remove(curvalues_d[vid])

  # Done: updateRelation

