class DetachedException(Exception):
    """If an operation is attempted on a Pulp object which requires an active client,
    and the object is not attached to any client, this exception is raised.
    """


class InvalidDataException(Exception):
    """Raised if raw Pulp data appears to be invalid (i.e. not matching expected schema).
    """


class PulpObject(object):
    """Base class for all modeled Pulp objects.

    Instances of PulpObject subclasses may be obtained by get and search methods
    on :class:`~pubtools.pulplib.Client`, or may be instantiated directly by calls
    to :meth:`from_data` when the client is not used.

    Objects which are created via a client may be used to issue further requests
    to Pulp (for example, to update or delete the object).

    Pulp objects use `attrs <http://www.attrs.org/en/stable/>`_.
    Attributes are immutable. Helper functions such as :func:`attr.evolve`
    may be used to produce new instances.

    Attributes exposed on these Pulp objects include some generic attributes
    applicable to any Pulp installation, but also some custom attributes
    which only make sense for `release-engineering <https://github.com/release-engineering>`_
    Pulp servers.
    """

    # Note: I'm not entirely sure this base class needs to exist.
    # It would mainly be used as a way of grouping certain documentation,
    # e.g. a place where we can document from_data only once instead of on each class.

    @classmethod
    def from_data(cls, data):
        """Obtain a detached instance using data obtained from Pulp.

        This method is provided so that callers who are not using
        :class:`~pubtools.pulplib.Client` may make use of the Pulp object classes.

        This method must be invoked on the appropriate ``PulpObject`` subclass
        matching ``data``.  For example, ``Repository.from_data`` must be invoked
        with a repository object provided by Pulp's API.

        Args:
            data (dict)
                A dict containing a raw representation of a Pulp object, as rendered
                by Pulp's API.

        Returns:
            a new instance of ``cls``

        Raises:
            InvalidDataException
                If the provided ``data`` fails validation against an expected schema.

        Example:

            Opting-out of using the ``Client`` class and instead doing a plain ``requests.get``:

            .. code-block:: python

                url = 'https://pulp.example.com/pulp/api/v2/repositories/zoo/'
                data = requests.get(url).json()
                repo = Repository.from_data(data)
        """
        # subclasses will be overriding this
        raise NotImplementedError("Must call from_data on concrete subclass!")


# Design notes
# ============
#
# All classes in this hierarchy are meant to be "attrs" classes. This can reduce
# the boilerplate and give us some nice advantages, such as immutability to discourage
# spaghetti code in callers.
#
# The classes are designed following the guideline here:
# http://www.attrs.org/en/stable/init.html
#
# This means that instances of these classes don't at all store the raw data passed
# in by Pulp, which has some implications:
#
# - there is no way to work around the API - if some attribute you need is missing from
#   a class, you can't peek at the raw data instead. You have to really add the attribute.
#
# - testing is easier because you can simply create a SomeObject(foo='a', bar='b') for any
#   given attributes, and not have to know/care about what that means in terms of how the
#   data is structured in Pulp
#
# Note that the initial version of these classes is fairly minimal. It is very much
# expected that many more attributes need to be added to these classes as we uncover
# use-cases for them.
#
# Regarding the validation of incoming data against schemas: those schemas would cover
# some generic Pulp fields, and some site-specific fields. They would be "open" schemas
# (i.e. unknown fields are allowed, but bad data in known fields is not allowed).
#
# It's hoped that the schemas could be encoded in .yaml files with full commentary,
# and those might be included in sphinx-generated docs. This could be used to replace
# some internal docs about the custom fields used on our Pulp servers.
#
