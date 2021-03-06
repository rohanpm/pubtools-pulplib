class Criteria(object):
    """Represents a Pulp search criteria.
    
    This is an opaque class which is not intended to be created
    or used directly. Instances of this class should be obtained and
    composed by calls to the documented class methods.

    Example:
        .. code-block:: python

            # With Pulp 2.x / mongo, this is roughly equivalent
            # to search fragment:
            #
            #  {"notes.my-field": {"$exists": True},
            #   "notes.other-field": {"$eq": ["a", "b", "c"]}}
            #
            crit = Criteria.and_(
                Criteria.with_field('notes.my-field', Criteria.exists),
                Criteria.with_field('notes.other-field', ["a", "b", "c"])
            )

            # criteria may now be used with client to execute a search
            repos = client.search_repository(crit)
    """

    exists = object()
    """
    Placeholder to denote that a field must exist, with no specific value.

    Example:

        .. code-block:: python

            # Would match any Repository where notes.my-field exists
            crit = Criteria.with_field('notes.my-field', Criteria.exists)
    """

    @classmethod
    def with_id(cls, ids):
        """Args:
            ids (str, list[str])
                An id or list of ids

        Returns:
            Criteria
                criteria for finding objects matching the given ID(s)
        """
        return cls.with_field("id", ids)

    @classmethod
    def with_field(cls, field_name, field_value):
        """Args:
            field_name (str)
                The name of a field.

                Field names may contain a "." to indicate nested fields,
                such as "notes.created".

            field_value (object)
                Any value, to be matched against the field.

        Returns:
            Criteria
                criteria for finding objects where ``field_name`` is present and
                matches ``field_value``.
        """

    @classmethod
    def and_(cls, *criteria):
        """Args:
            criteria (list[Criteria])
                Any number of criteria.

        Returns:
            :class:`Criteria`
                criteria for finding objects which satisfy all of the input ``criteria``.
        """

    @classmethod
    def or_(cls, *criteria):
        """Args:
            criteria (list[Criteria])
                Any number of criteria.

        Returns:
            Criteria
                criteria for finding objects which satisfy any of the input ``criteria``.
        """


# Design Notes
# ============
#
# Pulp 2.x uses mongo query fragments to expose a search API.
# These are the main reasons why we have these Criteria classes instead of just
# accepting arbitrary dicts for search:
#
# - To reduce the effort for callers of this library to later move to Pulp 3.x
#   which doesn't use mongo.  A query like {"id": {"$in": ["a", "b", "c"]}} is not
#   going to work with Pulp 3.  A query like Criteria.with_id(["a", "b", "c"]) could
#   potentially be made to work without the caller having to change.
#
# - To ensure that the FakeClient can be reasonably implemented. If searches use
#   mongo fragments, implementing an accurate fake client is impractical, since
#   callers could use the entire range of mongo features. By limiting the criteria,
#   we can ensure both the FakeClient and the real Client can perform searches with
#   whatever criteria may be passed by users.
#
# Criteria instances are expected to be used by the client roughly like this:
#
# - Client will build up a mongo query dict for any given Criteria
# - FakeClient will directly evaluate the Criteria against some in-memory repository objects
#
