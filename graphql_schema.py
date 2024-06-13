import graphene
import accounts.graphql_mutation
import accounts.graphql_schema
import organisation.graphql_schema
import organisation.graphql_mutation
import visitor.graphql_schema
import visitor.graphql_mutation

class Query(accounts.graphql_schema.Query, organisation.graphql_schema.Query, visitor.graphql_schema.Query, graphene.ObjectType):
    pass

class Mutation(accounts.graphql_mutation.Mutation  , organisation.graphql_mutation.Mutation, visitor.graphql_mutation.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
