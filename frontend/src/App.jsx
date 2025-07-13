import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Checkbox } from '@/components/ui/checkbox.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, TrendingUp, Users, Target } from 'lucide-react'
import './App.css'

function App() {
  const [formData, setFormData] = useState({
    phone_number: '',
    email: '',
    credit_score: '',
    age_group: '',
    family_background: '',
    income: '',
    comments: '',
    consent: false
  })

  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await fetch("https://60h5imcyy73y.manus.space/api/score", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          credit_score: parseInt(formData.credit_score),
          income: parseInt(formData.income)
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to score lead')
      }

      const result = await response.json()
      setLeads(prev => [result, ...prev])

      setFormData({
        phone_number: '',
        email: '',
        credit_score: '',
        age_group: '',
        family_background: '',
        income: '',
        comments: '',
        consent: false
      })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const getScoreBadgeVariant = (score) => {
    if (score >= 70) return 'default'
    if (score >= 40) return 'secondary'
    return 'destructive'
  }

  const getScoreLabel = (score) => {
    if (score >= 70) return 'High Intent'
    if (score >= 40) return 'Medium Intent'
    return 'Low Intent'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Lead Scoring Dashboard
          </h1>
          <p className="text-lg text-gray-600">
            Predict lead intent using machine learning and intelligent re-ranking
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Leads</CardTitle>
              <Users className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{leads.length}</div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">High Intent Leads</CardTitle>
              <Target className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {leads.filter(lead => lead.reranked_score >= 70).length}
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg. Score</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {leads.length > 0 
                  ? Math.round(leads.reduce((sum, lead) => sum + lead.reranked_score, 0) / leads.length)
                  : 0
                }
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <Card>
            <CardHeader>
              <CardTitle>Add New Lead</CardTitle>
              <CardDescription>
                Enter lead information to get an AI-powered intent score
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone Number</Label>
                    <Input
                      id="phone"
                      placeholder="+91-9876543210"
                      value={formData.phone_number}
                      onChange={(e) => handleInputChange('phone_number', e.target.value)}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="john.doe@example.com"
                      value={formData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="credit_score">Credit Score</Label>
                    <Input
                      id="credit_score"
                      type="number"
                      placeholder="750"
                      min="300"
                      max="850"
                      value={formData.credit_score}
                      onChange={(e) => handleInputChange('credit_score', e.target.value)}
                      required
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="income">Income (INR)</Label>
                    <Input
                      id="income"
                      type="number"
                      placeholder="500000"
                      min="0"
                      value={formData.income}
                      onChange={(e) => handleInputChange('income', e.target.value)}
                      required
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="age_group">Age Group</Label>
                    <Select value={formData.age_group} onValueChange={(value) => handleInputChange('age_group', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select age group" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="18-25">18-25</SelectItem>
                        <SelectItem value="26-35">26-35</SelectItem>
                        <SelectItem value="36-50">36-50</SelectItem>
                        <SelectItem value="51+">51+</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="family_background">Family Background</Label>
                    <Select value={formData.family_background} onValueChange={(value) => handleInputChange('family_background', value)}>
                      <SelectTrigger>
                        <SelectValue placeholder="Select family background" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="Single">Single</SelectItem>
                        <SelectItem value="Married">Married</SelectItem>
                        <SelectItem value="Married with Kids">Married with Kids</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="comments">Comments</Label>
                  <Textarea
                    id="comments"
                    placeholder="Any additional comments about the lead..."
                    value={formData.comments}
                    onChange={(e) => handleInputChange('comments', e.target.value)}
                    required
                  />
                </div>

                <div className="flex items-center space-x-2">
                  <Checkbox
                    id="consent"
                    checked={formData.consent}
                    onCheckedChange={(checked) => handleInputChange('consent', checked)}
                    required
                  />
                  <Label htmlFor="consent" className="text-sm">
                    I consent to data processing
                  </Label>
                </div>

                {error && (
                  <div className="text-red-600 text-sm">{error}</div>
                )}

                <Button type="submit" className="w-full" disabled={loading}>
                  {loading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Scoring Lead...
                    </>
                  ) : (
                    'Score Lead'
                  )}
                </Button>
              </form>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Scored Leads</CardTitle>
              <CardDescription>
                View all leads with their AI-generated scores
              </CardDescription>
            </CardHeader>
            <CardContent>
              {leads.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  No leads scored yet. Add a lead to get started.
                </div>
              ) : (
                <div className="overflow-auto max-h-96">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Email</TableHead>
                        <TableHead>Initial Score</TableHead>
                        <TableHead>Final Score</TableHead>
                        <TableHead>Intent</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {leads.map((lead, index) => (
                        <TableRow key={index}>
                          <TableCell className="font-medium">
                            {lead.email}
                          </TableCell>
                          <TableCell>
                            <Badge variant="outline">
                              {Math.round(lead.initial_score)}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <Badge variant={getScoreBadgeVariant(lead.reranked_score)}>
                              {Math.round(lead.reranked_score)}
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <span className={`text-sm font-medium ${
                              lead.reranked_score >= 70 ? 'text-green-600' :
                              lead.reranked_score >= 40 ? 'text-yellow-600' : 'text-red-600'
                            }`}>
                              {getScoreLabel(lead.reranked_score)}
                            </span>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default App
